import pygame

class Maze:
    def __init__(self, maze_data, screen_width, screen_height, top_margin=50):
        self.maze_data = maze_data
        self.rows = len(maze_data)
        self.cols = len(maze_data[0])
        self.top_margin = top_margin

        # 타일 크기 동적 설정 (화면 크기에 맞게 조정)
        max_tile_size_width = (screen_width - 20) // self.cols  # 좌우 여백 20
        max_tile_size_height = (screen_height - self.top_margin - 20) // self.rows  # 상단 여백 20
        self.tile_size = min(max_tile_size_width, max_tile_size_height)

        # 미로 전체 크기
        self.maze_width = self.tile_size * self.cols
        self.maze_height = self.tile_size * self.rows

        # 미로 중앙 정렬
        self.offset_x = (screen_width - self.maze_width) // 2
        self.offset_y = (screen_height - self.maze_height) // 2

    def render(self, screen, start, goal):
        """미로를 화면에 렌더링"""
        for row in range(self.rows):
            for col in range(self.cols):
                color = (255, 255, 255)  # 기본 경로 색
                if self.maze_data[row][col] == 1:  # 벽
                    color = (200, 162, 200) 
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(
                        self.offset_x + col * self.tile_size,
                        self.offset_y + row * self.tile_size,
                        self.tile_size,
                        self.tile_size,
                    )
                )

        # 시작점
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (
                self.offset_x + start[0] * self.tile_size,
                self.offset_y + start[1] * self.tile_size,
                self.tile_size,
                self.tile_size,
            ),
        )
        # 도착점 (파란색)
        pygame.draw.rect(
            screen,
            (0, 0, 255),
            (
                self.offset_x + goal[0] * self.tile_size,
                self.offset_y + goal[1] * self.tile_size,
                self.tile_size,
                self.tile_size,
            ),
        )
