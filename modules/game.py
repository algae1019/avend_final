import pygame
import random
from heapq import heappop, heappush
from modules.maze_generator import generate_maze
from modules.maze import Maze
from modules.player import Player
from modules.monster import Monster
from utils.path import get_path

class Game:
    def __init__(self, screen, w, h, stages=5):
        self.screen = screen
        self.screen_width = w
        self.screen_height = h
        self.current_stage = 1
        self.total_stages = stages
        self.hint_used = False
        self.start = (1, 1)
        self.maze_data = None
        self.maze = None
        self.player = None
        self.goal = None
        self.coins = []
        self.collected_coins = 0  # 수집된 코인 수 초기화
        self.player_path = []  # 플레이어의 이동 경로 저장
        self.monster = None
        self.vision_radius = 5  # 시야 제한 반경 (5단계용)
        self.coins_warning_shown = False  # 경고 메시지 출력 여부
        self.top_margin = 50
        self.monster_active = False  # 몬스터 활성화 플래그
        self.current_stage_cleared = False  # 단계 클리어 상태 초기화

        self.coin_sound = pygame.mixer.Sound(get_path('assets', 'coin.mp3')) # 경로 수정
        self.coin_sound.set_volume(0.3)
        self.monster_sound = pygame.mixer.Sound(get_path('assets', 'game_over.mp3'))
        self.monster_sound.set_volume(0.3)

    def next_stage(self):
        if self.current_stage > self.total_stages:
            print("Congratulations! You completed the game.")
            pygame.quit()
            exit()
        else:
            size = [11, 23, 33, 43, 55][self.current_stage - 1]
            self.maze_data = generate_maze(size, size)
            self.goal = (size - 2, size - 2)
            self.maze = Maze(self.maze_data, self.screen_width, self.screen_height, top_margin=self.top_margin)
            self.player = Player(start_pos=self.start, tile_size=self.maze.tile_size)
            self.player.set_offset(self.maze.offset_x, self.maze.offset_y)
            self.coins = self.place_coins() if self.current_stage >= 3 else []
            self.collected_coins = 0  # 새로운 스테이지에서 초기화
            self.coins_warning_shown = False  # 새로운 단계에서 경고 메시지 리셋
            self.player_path = []  # 경로 초기화
            self.current_stage_cleared = False

            if self.current_stage >= 4:
                self.monster_active = False
                self.monster = None
            print(f"Stage {self.current_stage} started!")


    def update_goal_reached(self):
        if (self.player.x, self.player.y) == self.goal:
            if self.current_stage >= 3 and self.coins:
                if not self.coins_warning_shown:  # 메시지가 아직 출력되지 않았다면
                    print("Collect all coins to finish!")
                    self.coins_warning_shown = True
            elif not self.coins:  # 코인을 모두 수집한 경우
                self.current_stage_cleared = True


    def place_coins(self):
        num_coins = [0, 0, 3, 5, 7][self.current_stage - 1]
        rows, cols = len(self.maze_data), len(self.maze_data[0])
        coins = []
        while len(coins) < num_coins:
            x, y = random.randint(1, cols - 2), random.randint(1, rows - 2)
            if self.maze_data[y][x] == 0 and (x, y) not in coins and (x, y) != self.start and (x, y) != self.goal:
                coins.append((x, y))
        return coins


    def record_player_path(self):
        """플레이어의 이동 경로 기록"""
        current_position = (self.player.x, self.player.y)
        if not self.player_path or self.player_path[-1] != current_position:
            self.player_path.append(current_position)  # 이동 경로 기록
            if self.monster:
                self.monster.path.append(current_position)  # 몬스터 경로 업데이트


    def render_coins(self):
        for x, y in self.coins:
            pygame.draw.circle(
                self.screen,
                (255, 215, 0),  # 금색 (Gold)
                (
                    self.maze.offset_x + x * self.maze.tile_size + self.maze.tile_size // 2,
                    self.maze.offset_y + y * self.maze.tile_size + self.maze.tile_size // 2,
                ),
                self.maze.tile_size // 4,
            )


    def render_vision(self):
        if self.current_stage == 5:
            surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            surface.fill((0, 0, 0))  # 완전히 검은색으로 채움

            # 플레이어의 픽셀 좌표를 기준으로 시야 중심 설정
            player_px = self.player.pixel_x + self.maze.tile_size // 2
            player_py = self.player.pixel_y + self.maze.tile_size // 2

            pygame.draw.circle(
                surface,
                (0, 0, 0, 0),  # 시야 범위는 투명
                (self.maze.offset_x + player_px, self.maze.offset_y + player_py),
                self.vision_radius * self.maze.tile_size,
            )
            self.screen.blit(surface, (0, 0))


    def collect_coin(self):
        player_px = self.player.pixel_x + self.maze.tile_size // 2
        player_py = self.player.pixel_y + self.maze.tile_size // 2

        for coin in self.coins:
            coin_px = coin[0] * self.maze.tile_size + self.maze.tile_size // 2
            coin_py = coin[1] * self.maze.tile_size + self.maze.tile_size // 2

            # 거리 계산
            distance = ((player_px - coin_px) ** 2 + (player_py - coin_py) ** 2) ** 0.5
            if distance < self.maze.tile_size * 0.5:  # 타일 절반 크기 이내라면 수집
                print(f"Coin collected at: {coin}")
                self.coins.remove(coin)  # 코인 제거
                self.collected_coins += 1
                self.coin_sound.play()
                break



    def update(self, keys):
        """게임 상태 업데이트"""
        self.player.update(keys, self.maze_data)

        # 플레이어가 출발하면 몬스터 활성화
        if not self.monster_active and (self.player.x, self.player.y) != self.start:
            self.activate_monster()

        self.record_player_path()  # 플레이어 경로 기록
        if self.monster:
            self.monster.update()  # 몬스터 이동

        # 충돌 확인
        if self.check_collision_with_monster():
            print("Game Over")

        self.collect_coin()  # 코인 수집 체크



    def render_status(self):
        font = pygame.font.SysFont("Arial", 24)

        # 스테이지 텍스트 (좌측 상단)
        stage_text = f"Stage: {self.current_stage}/{self.total_stages}"
        stage_surface = font.render(stage_text, True, (255, 255, 255))
        self.screen.blit(stage_surface, (10, 10))  # 좌측 상단

        # 코인 텍스트 (우측 상단, 3단계 이상에서만 표시)
        if self.current_stage >= 3:
            total_coins = [0, 0, 3, 5, 7][self.current_stage - 1]
            coins_text = f"Coins: {self.collected_coins}/{total_coins}"
            coins_surface = font.render(coins_text, True, (255, 255, 255))
            # 우측 상단에 표시
            text_width = coins_surface.get_width()
            self.screen.blit(coins_surface, (self.screen_width - 10 - text_width, 10))  # 오른쪽 상단

    
    def check_collision_with_monster(self):
        """플레이어와 몬스터의 충돌 확인"""
        if self.monster:
            player_px = self.player.pixel_x + self.maze.tile_size // 2
            player_py = self.player.pixel_y + self.maze.tile_size // 2

            monster_px = self.monster.pixel_x + self.maze.tile_size // 2
            monster_py = self.monster.pixel_y + self.maze.tile_size // 2

            # 거리 계산
            distance = ((player_px - monster_px) ** 2 + (player_py - monster_py) ** 2) ** 0.5
            if distance < self.maze.tile_size * 0.5:  # 충돌 조건
                self.monster_sound.play()
                return True
        return False
    

    def activate_monster(self):
        """몬스터 활성화"""
        if not self.monster_active and self.current_stage >= 4:
            self.monster_active = True
            self.monster = Monster(
                start_position=self.start,
                tile_size=self.maze.tile_size,
                offset_x=self.maze.offset_x,
                offset_y=self.maze.offset_y
            )
            print("Monster activated!")

    from heapq import heappop, heappush


    def heuristic(self, a, b):
        """맨해튼 거리 계산"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


    def reconstruct_path(self, came_from, current):
        """A* 알고리즘으로 계산된 경로를 재구성"""
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path


    def astar(self, maze, start, goal):
        """A* 알고리즘을 사용해 최단 경로를 계산"""
        rows, cols = len(maze), len(maze[0])
        open_set = []
        heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            _, current = heappop(open_set)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[1]][neighbor[0]] == 0:
                    tentative_g_score = g_score[current] + 1
                    if tentative_g_score < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                        if neighbor not in [item[1] for item in open_set]:
                            heappush(open_set, (f_score[neighbor], neighbor))

        return []  # 경로가 없을 경우 빈 리스트 반환

    

    def use_hint(self):
        """힌트를 사용하여 현재 위치에서 도착지점까지 최단 경로를 3초 동안 표시"""
        if self.hint_used:
            print("Hint already used.")
            return

        self.hint_used = True
        path = self.astar(self.maze_data, (self.player.x, self.player.y), self.goal)
        if not path:
            print("No path found!")
            return

        print("Hint used: Displaying shortest path.")

        # 화면을 새로 렌더링하면서 힌트를 표시
        for _ in range(180):  # 약 3초 동안 (60 FPS 기준)
            self.maze.render(self.screen, self.start, self.goal)  # 미로 렌더링

            # 경로 하이라이트 (플레이어, 몬스터, 코인 렌더링 전)
            for x, y in path:
                pygame.draw.rect(
                    self.screen,
                    (0, 255, 255),  # 하늘색으로 강조
                    (
                        self.maze.offset_x + x * self.maze.tile_size,
                        self.maze.offset_y + y * self.maze.tile_size,
                        self.maze.tile_size,
                        self.maze.tile_size,
                    )
                )

            self.render_coins()  # 코인 렌더링
            if self.monster:
                self.monster.render(self.screen)  # 몬스터 렌더링
            self.player.render(self.screen)  # 플레이어 렌더링 (가장 위에)

            pygame.display.flip()
            pygame.time.delay(16)  # 약 60 FPS 유지
