import random

def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]

    def carve(x, y):
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                maze[ny][nx] = 0
                maze[y + dy // 2][x + dx // 2] = 0
                carve(nx, ny)

    # 시작점 설정
    maze[1][1] = 0
    carve(1, 1)
    return maze