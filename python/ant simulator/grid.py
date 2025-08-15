class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)] # 0 = white

    def update_value(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = value

    def get_value(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None
    
    @property
    def rows(self):
        return self.height

    @property
    def cols(self):
        return self.width

    def render(self):
        for row in self.grid:
            print(' '.join(['█' if cell == 1 else ' ' for cell in row]))