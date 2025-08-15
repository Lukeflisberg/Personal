import pygame
import pygame_gui
import random
import sys

from grid import Grid
from ant import Ant

# Set up display
width, height = 800, 800

# Create a grid instance
grid = Grid(256, 256)

cell_width = width // grid.cols
cell_height = height // grid.rows

# Define color map
COLOR_MAP = {
    0: (255, 255, 255),  # white
    1: (0, 0, 0),        # black
    2: (0, 255, 0),      # green
    3: (255, 0, 0),      # red
    4: (0, 0, 255),      # blue
    5: (255, 255, 0),    # yellow
    6: (0, 255, 243)     # turqois
}

# Create ants
ants = []
nr_ants = int(input("Enter number of ants (max6): "))

if nr_ants in range(1, 7):
    for i in range(1, nr_ants+1):
        ants.append(Ant(grid, (random.randint(0, 255), random.randint(0, 255)), i))
else:
    exit("Invalid number of ants.")

# Initialize Pygame
pygame.init()

# Create the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Grid Visualization")

# Set up pygame_gui
manager = pygame_gui.UIManager((width, height))
slider_rect = pygame.Rect(10, height - 60, 300, 40)
speed_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=slider_rect,
    start_value=0,
    value_range=(0, 100),
    manager=manager
)

clock = pygame.time.Clock()

# Main loop
while True:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        manager.process_events(event)
    
    # Update slider value
    manager.update(time_delta)
    speed = int(speed_slider.get_current_value()) + 1  # +1 to avoid zero

    # Update ants
    for _ in range(speed):
        for ant in ants:
            ant.update()

    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Draw the grid
    for y in range(grid.rows):
        for x in range(grid.cols):
            color_id = grid.get_value(x, y)
            color = COLOR_MAP.get(color_id, (255, 255, 255))
            pygame.draw.rect(screen, color, (x * cell_width, y * cell_height, cell_width, cell_height))

    # Draw the slider
    manager.draw_ui(screen)

    pygame.display.flip()