import pygame
from utils.path import get_path

def main_menu(screen, window_size):
    """메인 메뉴 화면"""
    # 배경 이미지 로드
    w, h = window_size
    background_image = pygame.image.load(get_path('assets', 'background.jpg'))
    stretched_background = pygame.transform.scale(background_image, (w, h))

    font = pygame.font.SysFont("Arial", 48)
    title_surface = font.render("Maze Game", True, (255, 255, 255))
    start_surface = font.render("Press ENTER to Start", True, (200, 200, 200))

    running = True
    while running:
        screen.blit(stretched_background, (0, 0))  # 배경 이미지 렌더링
        screen.blit(title_surface, (250, 200))  # 타이틀 위치
        screen.blit(start_surface, (180, 400))  # 시작 메시지 위치
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return  # ENTER 키로 게임 시작

def game_over_screen(screen):
    """게임 오버 화면"""
    font = pygame.font.SysFont("Arial", 48)
    message_surface = font.render("Game Over", True, (255, 0, 0))
    restart_surface = font.render("Press Enter to Restart", True, (200, 200, 200))

    running = True
    while running:
        screen.fill((0, 0, 0))  # 배경색
        screen.blit(message_surface, (250, 200))  # 메시지 위치
        screen.blit(restart_surface, (180, 400))  # 재시작 메시지 위치
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # R 키로 재시작

def stage_clear_screen(screen, stage_number):
    """단계 클리어 화면"""
    font = pygame.font.SysFont("Arial", 48)
    message_surface = font.render(f"Stage {stage_number} Clear!", True, (255, 255, 0))
    continue_surface = font.render("Press ENTER to Continue", True, (200, 200, 200))

    running = True
    while running:
        screen.fill((0, 0, 0))  # 배경색
        screen.blit(message_surface, (200, 200))  # 클리어 메시지 위치
        screen.blit(continue_surface, (150, 400))  # 계속 메시지 위치
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return  # ENTER 키로 다음 단계 진행
