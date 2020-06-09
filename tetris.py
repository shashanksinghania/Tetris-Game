import pygame
import random

window_height = 700
window_width = 800

# To keep the play grid dimensions in a 2:1 ratio
grid_height = 600
grid_width = 300

cube_side = 30

# Co-ordinates of the playing grid on the window:
x_coordinate = (window_width - grid_width) // 2
y_coordinate = window_height - grid_height

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

pieces = [S, Z, I, O, J, L, T]
piece_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = piece_colors[pieces.index(shape)]
        self.rotation = 0


def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for x in range(grid_width // cube_side)] for x in range(grid_height // cube_side)]
    for i, j in locked_pos.keys():
        grid[j][i] = locked_pos[(i, j)]
    return grid


def get_random_piece():
    return Piece(5, 0, random.choice(pieces))


def draw_grid(window, grid):

    # Grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(window, grid[i][j], (x_coordinate + cube_side * j, y_coordinate + cube_side * i, cube_side, cube_side), 0)

    # Border
    pygame.draw.rect(window, (255, 0, 0), (x_coordinate, y_coordinate, grid_width, grid_height), 4)


def draw_window(window, grid):
    # Background color
    window.fill((0, 0, 0))

    # Title Text
    pygame.font.init()
    fnt = pygame.font.SysFont("Commicsans", 60)
    txt = fnt.render("Tetris", 1, (255, 255, 255))
    window.blit(txt, ((window_width - txt.get_width()) // 2, 30))

    draw_grid(window, grid)

    pygame.display.update()




def main():
    locked_pos = {}
    grid = create_grid(locked_pos)
    current_piece = get_random_piece()
    next_piece = get_random_piece()
    fall_time = 0
    change_piece = False
    run = True
    clock = pygame.time.Clock()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1

