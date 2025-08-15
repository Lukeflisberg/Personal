# You have the ability to "spawn" ants
# Each ant will do the following
# > Pick a random direction(up, down, left, right) and move one block in said direction)
# > When an ant moves onto a colored2 block, it will turn it into a colored1 block. If it moves onto a colored1 block, it will turn into a colored2 block
# These blocks will be displayed on a gridless grid
# The user will able to effect the simulation by:
# > Using a slider to effect speed
# > Being able to set the color of the ants
# > Being able to set a radius
# > Being able to change the way the ant moves

class Ant:
    def __init__(self, grid, position, color_id):
        self.grid = grid
        self.x, self.y = position
        self.color_id = color_id

    def update(self):
        import random

        dx, dy = random.choice([(0,1), (1,0), (0,-1), (-1,0)])
        nx, ny = self.x + dx, self.y + dy

        if 0 <= nx < self.grid.cols and 0 <= ny < self.grid.rows:
            self.x, self.y = nx, ny

            current_color = self.grid.get_value(self.x, self.y)
            self.grid.update_value(self.x, self.y, 0 if current_color == self.color_id else self.color_id)