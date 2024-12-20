import pygame

class Player:
    def __init__(self, start_pos=(1, 1), tile_size=40):
        self.x, self.y = start_pos  # 현재 좌표 (미로 데이터 좌표)
        self.target_x, self.target_y = self.x, self.y  # 목표 좌표
        self.tile_size = tile_size
        self.color = (0, 128, 0) 
        self.offset_x = 0  # 화면 오프셋 X
        self.offset_y = 0  # 화면 오프셋 Y
        self.speed = 5  # 애니메이션 속도 (픽셀/프레임)

        self.moving = False  # 이동 상태
        self.last_input_time = pygame.time.get_ticks()  # 마지막 입력 시간 초기화
        self.input_delay = 100  # 입력 딜레이 (밀리초)
        self.pixel_x = self.x * self.tile_size  # 화면 픽셀 좌표 X
        self.pixel_y = self.y * self.tile_size  # 화면 픽셀 좌표 Y

    def set_offset(self, offset_x, offset_y):
        self.offset_x = offset_x
        self.offset_y = offset_y

    def find_next_stop(self, direction, maze):
        """다음 분기점 또는 벽 위치를 찾음"""
        dx, dy = direction
        nx, ny = self.x, self.y

        while True:
            nx += dx
            ny += dy
            if not (0 <= nx < len(maze[0]) and 0 <= ny < len(maze)):  # 경계 밖
                return nx - dx, ny - dy
            if maze[ny][nx] == 1:  # 벽
                return nx - dx, ny - dy
            # 분기점 조건: 상하좌우 중 갈림길인지 확인
            valid_paths = sum(
                1 for dx2, dy2 in [(0, -1), (0, 1), (-1, 0), (1, 0)]
                if 0 <= nx + dx2 < len(maze[0]) and 0 <= ny + dy2 < len(maze) and maze[ny + dy2][nx + dx2] == 0
            )
            if valid_paths > 2:  # 2개 이상의 선택지가 있는 경우 분기점
                return nx, ny

    def update(self, keys, maze):
        current_time = pygame.time.get_ticks()

        if not self.moving:
            # 입력 딜레이 확인
            if current_time - self.last_input_time < self.input_delay:
                return

            # 이동 방향 설정
            direction = None
            if keys[pygame.K_UP]:
                direction = (0, -1)
            elif keys[pygame.K_DOWN]:
                direction = (0, 1)
            elif keys[pygame.K_LEFT]:
                direction = (-1, 0)
            elif keys[pygame.K_RIGHT]:
                direction = (1, 0)

            if direction:
                # 다음 목표 좌표 설정
                self.target_x, self.target_y = self.find_next_stop(direction, maze)
                self.moving = True
                self.last_input_time = current_time  # 입력 시간 기록

        if self.moving:
            # 애니메이션 이동 처리
            target_px = self.target_x * self.tile_size
            target_py = self.target_y * self.tile_size

            if self.pixel_x < target_px:
                self.pixel_x = min(self.pixel_x + self.speed, target_px)
            elif self.pixel_x > target_px:
                self.pixel_x = max(self.pixel_x - self.speed, target_px)
            if self.pixel_y < target_py:
                self.pixel_y = min(self.pixel_y + self.speed, target_py)
            elif self.pixel_y > target_py:
                self.pixel_y = max(self.pixel_y - self.speed, target_py)

            # 이동 완료 확인
            if self.pixel_x == target_px and self.pixel_y == target_py:
                self.x, self.y = self.target_x, self.target_y
                self.moving = False


    def render(self, screen):
        # 화면 렌더링 (초록색 원으로 표시, 크기 확대)
        pygame.draw.circle(
            screen,
            self.color,
            (
                self.offset_x + self.pixel_x + self.tile_size // 2,
                self.offset_y + self.pixel_y + self.tile_size // 2,
            ),
            self.tile_size // 2 - 2,  # 원의 반지름을 타일 크기보다 약간 작게 설정
        )