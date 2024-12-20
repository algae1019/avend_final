import pygame
from modules.game import Game
from modules.menu import main_menu, game_over_screen, stage_clear_screen
from utils.path import get_path

def main():
    pygame.init()

    # 화면 설정
    SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 840
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Game")

    main_menu(screen, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Game 객체 초기화
    game = Game(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    game.next_stage()

    pygame.mixer.init()
    pygame.mixer.music.load(get_path('assets', 'background_music.mp3'))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:  # H 키로 힌트 사용
                    game.use_hint()

        keys = pygame.key.get_pressed()
        game.update(keys)  # 게임 상태 업데이트
        game.record_player_path()  # 플레이어 이동 경로 기록
        if game.monster:
            game.monster.update()  # 몬스터 이동
        game.collect_coin()  # 코인 수집 로직


        if game.check_collision_with_monster():
            pygame.mixer.music.stop()
            game_over_screen(screen)  # 충돌 시 게임 오버 화면
            main_menu(screen, (SCREEN_WIDTH, SCREEN_HEIGHT))  # 게임 오버 후 메인 메뉴로 돌아감
            game = Game(screen, SCREEN_WIDTH, SCREEN_HEIGHT)  # 게임 객체 재설정
            game.next_stage()
            pygame.mixer.music.play(-1)

        game.update_goal_reached()  # 도착지점 관련 로직 처리

        # 단계 클리어 처리
        if game.current_stage_cleared:
            stage_clear_screen(screen, game.current_stage)
            game.current_stage += 1
            game.next_stage()

        # 화면 그리기
        screen.fill((0, 0, 0))
        game.render_status()  # 상단 상태 정보 렌더링
        game.maze.render(screen, game.start, game.goal)
        game.render_coins()
        if game.monster:
            game.monster.render(screen)  # 몬스터 렌더링
        if game.current_stage == 5:
            game.render_vision()  # 시야 제한 적용
        game.player.render(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
