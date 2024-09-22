import sys
import pygame
from random import sample

SCREEN_HEIGHT, SCREEN_WIDTH = 550, 550
PUZZLE_SIZE = 9
BOX_SIZE = 3
BACKGROUND_COLOR = (251, 247, 245)
RECT_COLOR = (255, 0, 0)
LINE_COLOR = (0, 0, 0)
CELL_FONT = ''
CELL_COLOR_ORIGINAL = (52, 31, 151)
CELL_COLOR_NEW = (0, 0, 0)
BUFFER = 5

grid_original = [[0 for _ in range(PUZZLE_SIZE)] for _ in range(PUZZLE_SIZE)]
grid = grid_original
list_cell_pos = []
list_empty_pos = []


# pattern for a baseline valid solution
# def pattern(r, c):
#     return (BOX_SIZE * (r % BOX_SIZE) + r // BOX_SIZE + c) % PUZZLE_SIZE


# randomize rows, columns and numbers (of valid base pattern)
# def shuffle(s):
#     return sample(s, len(s))


# def generate_sudoku_puzzle():
#     boxes = range(BOX_SIZE)
#     rows = [g * BOX_SIZE + r for g in shuffle(boxes) for r in shuffle(boxes)]
#     cols = [g * BOX_SIZE + c for g in shuffle(boxes) for c in shuffle(boxes)]
#     nums = shuffle(range(1, BOX_SIZE * BOX_SIZE + 1))
#
#     # produce board using randomized baseline pattern
#     global grid_original
#     grid_original = [[nums[pattern(r, c)] for c in cols] for r in rows]
#     for line in grid_original:
#         print(line)
#
#     squares = 81
#     empties = squares * 4 // 4
#     for p in sample(range(squares), empties):
#         grid_original[p // PUZZLE_SIZE][p % PUZZLE_SIZE] = 0
#
#     global grid
#     grid = [[grid_original[row][col] for col in range(PUZZLE_SIZE)] for row in range(PUZZLE_SIZE)]
#     for line in grid:
#         print(line)


def generate_cells(cell_index):
    if cell_index == len(list_cell_pos):
        return True

    list_nums = sample(range(1, 10), 9)
    cell_row, cell_col = list_cell_pos[cell_index]
    for ele in list_nums:
        if is_valid((cell_row, cell_col), ele) is True:
            grid[cell_row][cell_col] = ele
            if generate_cells(cell_index + 1) is True:
                return True
            grid[cell_row][cell_col] = 0

    return False


def generate_sudoku_puzzle():
    global list_cell_pos
    for cell_row in range(PUZZLE_SIZE):
        for cell_col in range(PUZZLE_SIZE):
            list_cell_pos.append((cell_row, cell_col))

    generate_cells(0)
    for row in grid:
        print(row)

    cells = 81
    empties = 60
    for pos in sample(range(cells), empties):
        grid[pos // PUZZLE_SIZE][pos % PUZZLE_SIZE] = 0

    global grid_original
    grid_original = [[grid[row][col] for col in range(PUZZLE_SIZE)] for row in range(PUZZLE_SIZE)]
    for row in grid_original:
        print(row)


def create_game():
    global CELL_FONT
    CELL_FONT = pygame.font.SysFont('Comic Sans MS', 35)
    pygame.display.set_caption('Sudoku')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(BACKGROUND_COLOR)

    for line in range(10):
        line_width = 4 if line % 3 == 0 else 2
        pygame.draw.line(screen, LINE_COLOR, (50 + 50 * line, 50), (50 + 50 * line, 500), line_width)
        pygame.draw.line(screen, LINE_COLOR, (50, 50 + 50 * line), (500, 50 + 50 * line), line_width)
    pygame.display.update()

    for row in range(PUZZLE_SIZE):
        for col in range(PUZZLE_SIZE):
            if grid[row][col] > 0:
                value = CELL_FONT.render(str(grid[row][col]), True, CELL_COLOR_ORIGINAL)
                screen.blit(value, ((col + 1) * 50 + 15, (row + 1) * 50))
    pygame.display.update()
    return screen


def is_valid(position, num):
    for col in range(PUZZLE_SIZE):
        if grid[position[0]][col] == num:
            return False

    for row in range(PUZZLE_SIZE):
        if grid[row][position[1]] == num:
            return False

    box_row = position[0] // BOX_SIZE * BOX_SIZE
    box_col = position[1] // BOX_SIZE * BOX_SIZE
    for row in range(BOX_SIZE):
        for col in range(BOX_SIZE):
            if grid[box_row + row][box_col + col] == num:
                return False

    return True


def find_empty_cell():
    global list_empty_pos
    for row in range(PUZZLE_SIZE):
        for col in range(PUZZLE_SIZE):
            if grid[row][col] == 0:
                list_empty_pos.append((row, col))


def sudoku_solver(screen, cell_index):
    if cell_index == len(list_empty_pos):
        return True

    cell_row, cell_col = list_empty_pos[cell_index]
    for num in range(1, PUZZLE_SIZE + 1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if is_valid((cell_row, cell_col), num):
            grid[cell_row][cell_col] = num
            value = CELL_FONT.render(str(num), True, CELL_COLOR_NEW)
            screen.blit(value, ((cell_col + 1) * 50 + 15, (cell_row + 1) * 50))
            pygame.display.update()
            # pygame.time.delay(25)

            if sudoku_solver(screen, cell_index + 1) is True:
                return True

            grid[cell_row][cell_col] = 0
            pygame.draw.rect(screen, BACKGROUND_COLOR,
                             ((cell_col + 1) * 50 + BUFFER, (cell_row + 1) * 50 + BUFFER, 50 - 2 * BUFFER,
                              50 - 2 * BUFFER))
            pygame.display.update()

    return False


def play_game(screen):
    running = True
    row, col = 0, 0
    while running:
        pygame.draw.rect(screen, RECT_COLOR,
                         (col * 50, row * 50, 52, 52), 4)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // 50, pos[0] // 50
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    global list_empty_pos
                    list_empty_pos = []
                    find_empty_cell()
                    if len(list_empty_pos) > 0:
                        print('Solving!!!')
                        sudoku_solver(screen, 0)
                if row < 1 or row > PUZZLE_SIZE or col < 1 or col > PUZZLE_SIZE:
                    continue
                if grid_original[row - 1][col - 1] > 0:
                    continue
                if event.key == pygame.K_0 or event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    grid[row - 1][col - 1] = 0
                    pygame.draw.rect(screen, BACKGROUND_COLOR,
                                     (col * 50 + BUFFER, row * 50 + BUFFER, 50 - 2 * BUFFER, 50 - 2 * BUFFER))
                    pygame.display.update()
                if 0 < event.key - 48 < 10:
                    grid[row - 1][col - 1] = event.key - 48
                    pygame.draw.rect(screen, BACKGROUND_COLOR,
                                     (col * 50 + BUFFER, row * 50 + BUFFER, 50 - 2 * BUFFER, 50 - 2 * BUFFER))
                    value = CELL_FONT.render(str(event.key - 48), True, CELL_COLOR_NEW)
                    screen.blit(value, (col * 50 + 15, row * 50))
                    pygame.display.update()

    print('End Game!!!')


def main():
    generate_sudoku_puzzle()
    pygame.init()
    screen = create_game()

    play_game(screen)
    pygame.quit()


if __name__ == '__main__':
    main()
