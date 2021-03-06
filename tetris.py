import pygame, sys
import random

pygame.font.init()

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

def display_end_message(window, text, size, color):
    font =pygame.font.SysFont("commicsans", size, bold=True)
    label = font.render(text, 1, color)

    window.blit(label, (x_coordinate + grid_width//2 - label.get_width()//2,
                         y_coordinate + grid_height//2 - label.get_height()//2))

def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for x in range(grid_width // cube_side)] for x in range(grid_height // cube_side)]
    for i, j in locked_pos.keys():
        grid[j][i] = locked_pos[(i, j)]
    return grid


def get_random_piece():
    return Piece(5, 0, random.choice(pieces))


def draw_grid_lines(window, grid):
    for i in range(len(grid)):
        pygame.draw.line(window, (128, 128, 128), (x_coordinate, y_coordinate + i * cube_side),
                         (x_coordinate + grid_width, y_coordinate + i * cube_side))
        for j in range(len(grid[i])):
            pygame.draw.line(window, (128, 128, 128), (x_coordinate + j * cube_side, y_coordinate),
                             (x_coordinate + j * cube_side, y_coordinate + grid_height))


def format_piece(piece):
    shape = piece.shape
    positions = []
    format = shape[piece.rotation % len(shape)]

    '''['.....',
        '..0..',
        '.00..',
        '..0..',
        '.....']'''

    for i, row in enumerate(format):
        for j, col in enumerate(row):
            if col == '0':
                positions.append((piece.x + j - 2, piece.y + i - 4))  # 2, 4 to adjust the positions

    return positions


def draw_next_piece(piece, window):
    right_side_x = x_coordinate + grid_width + 50
    right_side_y = y_coordinate + 70

    fnt = pygame.font.SysFont('commicsans', 35)
    txt = fnt.render("Next Shape", 1, (255, 255, 255))
    window.blit(txt, (right_side_x + 10, right_side_y))

    # Shape
    shape = piece.shape
    positions = shape[piece.rotation % len(shape)]

    for x, row in enumerate(positions):
        for y, col in enumerate(row):
            if col == '0':
                pygame.draw.rect(window, piece.color,
                                 (right_side_x + 10 + x * cube_side, right_side_y + 30 + y * cube_side,
                                  cube_side, cube_side), 0)


def draw_window(window, grid, score=0):

    # Background color
    window.fill((0, 0, 0))

    # Title Text
    pygame.font.init()
    fnt = pygame.font.SysFont("Commicsans", 60)
    txt = fnt.render("Tetris", 1, (255, 255, 255))
    window.blit(txt, ((window_width - txt.get_width()) // 2, 30))

    # Grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(window, grid[i][j],
                             (x_coordinate + cube_side * j, y_coordinate + cube_side * i, cube_side, cube_side), 0)

    # Border
    pygame.draw.rect(window, (255, 0, 0), (x_coordinate, y_coordinate, grid_width, grid_height), 4)

    draw_grid_lines(window, grid)

    right_side_x = x_coordinate + grid_width + 50
    right_side_y = y_coordinate + 70

    fnt = pygame.font.SysFont('commicsans', 35)
    txt = fnt.render("Score: "+ str(score), 1, (255, 255, 255))
    window.blit(txt, (right_side_x + 30, right_side_y + 200))


def is_valid_pos(piece, grid):
    valid_positions = []

    # all valid positions
    for i in range(10):
        for j in range(20):
            if grid[j][i] == (0, 0, 0):
                valid_positions.append((i, j))

    formatted = format_piece(piece)
    for ele in formatted:
        if ele not in valid_positions:
            if ele[1] > -1:
                return False
    return True


def clear_rows(grid, locked_pos):
    num_of_rows = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            num_of_rows += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked_pos[(j, i)]
                except:
                    continue

    # If we have removed at least 1 row
    if num_of_rows > 0:
        for key in sorted(list(locked_pos), key=lambda k: k[1], reverse=True):
            x, y = key
            if y < ind:
                key1 = (x, y + num_of_rows)
                locked_pos[key1] = locked_pos.pop(key)
    return num_of_rows


def check_lost(positions):
    for x, y in positions:
        if y < 1:
            return True
    return False


def main(window):
    score = 0
    locked_pos = {}
    current_piece = get_random_piece()
    next_piece = get_random_piece()
    fall_time = 0
    fall_speed = 0.27
    lock_piece = False
    run = True
    clock = pygame.time.Clock()

    while run:
        grid = create_grid(locked_pos)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not is_valid_pos(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                lock_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not is_valid_pos(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not is_valid_pos(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not is_valid_pos(current_piece, grid):
                        current_piece.rotation -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not is_valid_pos(current_piece, grid):
                        current_piece.y -= 1

        shape_pos = format_piece(current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if lock_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_pos[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_random_piece()
            lock_piece = False
            score += 100 * clear_rows(grid, locked_pos)

        draw_window(window, grid, score)
        draw_next_piece(next_piece, window)
        pygame.display.update()

        if check_lost(locked_pos):
            display_end_message(window, "GAME OVER!", 80, (255, 215, 0))
            pygame.display.update()
            pygame.time.delay(2000)
            run = False


def main_menu(window):
    run = True
    while run:
        window.fill((0, 0, 0))
        display_end_message(window, 'Press Any Key To Play', 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(window)

    pygame.display.quit()


surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Tetris")
main_menu(surface)
