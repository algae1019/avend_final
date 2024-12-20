import pygame

class Monster:
    def __init__(self, start_position, tile_size, offset_x, offset_y):
        """
        몬스터 초기화
        :param start_position: 몬스터 시작 위치 (x, y)
        :param tile_size: 타일 크기
        :param offset_x: 화면 오프셋 X
        :param offset_y: 화면 오프셋 Y
        """
        self.position = start_position  # 현재 타일 좌표
        self.pixel_x = start_position[0] * tile_size  # 픽셀 좌표 X
        self.pixel_y = start_position[1] * tile_size  # 픽셀 좌표 Y
        self.tile_size = tile_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.path = []  # 몬스터가 이동할 경로
        self.speed = 1  # 이동 속도 (픽셀 단위)

    def update(self):
        """몬스터가 경로를 따라 이동"""
        if self.path:
            target = self.path[0]  # 경로의 첫 번째 목표 지점
            target_px = target[0] * self.tile_size
            target_py = target[1] * self.tile_size

            # X 축 이동
            if self.pixel_x < target_px:
                self.pixel_x = min(self.pixel_x + self.speed, target_px)
            elif self.pixel_x > target_px:
                self.pixel_x = max(self.pixel_x - self.speed, target_px)

            # Y 축 이동
            if self.pixel_y < target_py:
                self.pixel_y = min(self.pixel_y + self.speed, target_py)
            elif self.pixel_y > target_py:
                self.pixel_y = max(self.pixel_y - self.speed, target_py)

            # 목표 지점에 도달하면 경로에서 제거
            if self.pixel_x == target_px and self.pixel_y == target_py:
                self.position = self.path.pop(0)

    def render(self, screen):
        """
        몬스터 렌더링
        :param screen: Pygame 화면 객체
        """
        pygame.draw.circle(
            screen,
            (255, 0, 0),  # 빨간색
            (
                self.offset_x + self.pixel_x + self.tile_size // 2,
                self.offset_y + self.pixel_y + self.tile_size // 2,
            ),
            self.tile_size // 2 - 4,  # 몬스터 크기
        )
