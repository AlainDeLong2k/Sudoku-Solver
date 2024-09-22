import pygame
import sys
import random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 540
SCREEN_HEIGHT = 600
GRID_SIZE = 60
FPS = 30

# Fonts
font = pygame.font.Font(None, 40)


def draw_grid(screen):
    for i in range(0, 10):
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (50, i * GRID_SIZE), (530, i * GRID_SIZE), 4)
            pygame.draw.line(screen, BLACK, (i * GRID_SIZE + 50, 0), (i * GRID_SIZE + 50, 540), 4)
        else:
            pygame.draw.line(screen, BLACK, (50, i * GRID_SIZE), (530, i * GRID_SIZE), 2)
            pygame.draw.line(screen, BLACK, (i * GRID_SIZE + 50, 0), (i * GRID_SIZE + 50, 540), 2)


def draw_numbers(screen, board):
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                text_surface = font.render(str(board[i][j]), True, BLACK)
                screen.blit(text_surface, (j * GRID_SIZE + 70, i * GRID_SIZE + 10))


# Các hàm khác không cần thay đổi
def generate_board():
    # Generate a solved Sudoku board
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve_sudoku(board)

    # Randomly remove numbers to create a puzzle
    num_of_empty_cells = random.randint(40, 50)
    for _ in range(num_of_empty_cells):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        board[row][col] = 0

    return board


def is_valid_move(board, row, col, num):
    for i in range(9):
        if board[i][col] == num or board[row][i] == num:
            return False
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True


def solve_sudoku(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if is_valid_move(board, i, j, num):
                        board[i][j] = num
                        if solve_sudoku(board):
                            return True
                        board[i][j] = 0
                return False
    return True


def main(screen):
    clock = pygame.time.Clock()
    board = generate_board()

    while True:
        screen.fill(WHITE)
        draw_grid(screen)
        draw_numbers(screen, board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    board = generate_board()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sudoku Game")
    main(screen)