import sys
import pygame
from random import randint, sample


class Board:
    PUZZLE_SIZE = 9
    COLOR_WHITE = (251, 247, 245)
    COLOR_BLACK = (0, 0, 0)
    BUFFER = 5

    def __init__(self, num_empties):
        self.original_board = [[0] * 9 for _ in range(9)]
        self.board = [[0] * 9 for _ in range(9)]
        self.empty = num_empties
        self.list_empty = []
        self.font = pygame.font.SysFont('Comic Sans MS', 35)
        self.generate_board()

    def generate_board(self):
        self.fill_all_boxes(0)
        self.remove_elements()

    def fill_all_boxes(self, cell_index):
        if cell_index == self.PUZZLE_SIZE * self.PUZZLE_SIZE:
            return True

        cell_row, cell_col = cell_index // 9, cell_index % 9
        list_nums = sample(range(1, 10), 9)
        for num in list_nums:
            if self.safe_to_fill(cell_row, cell_col, num):
                self.board[cell_row][cell_col] = num
                if self.fill_all_boxes(cell_index + 1) is True:
                    return True
                self.board[cell_row][cell_col] = 0

        return False

    def remove_elements(self):
        while self.empty != 0:
            index = randint(0, 80)
            row, col = index // 9, index % 9
            while self.board[row][col - 1 if col != 0 else col] == 0:
                index = randint(0, 80)
                row, col = int(index / 9), index % 9 - 1
            self.board[row][col - 1 if col != 0 else col] = 0
            self.empty -= 1

        self.original_board = [[self.board[row][col] for col in range(self.PUZZLE_SIZE)] for row in
                               range(self.PUZZLE_SIZE)]

    # Check entire row whether a number is used
    def row_is_safe(self, row, num):
        for i in range(9):
            if self.board[row][i] == num:
                return False
        return True

    # Check entire column whether a number is used
    def col_is_safe(self, col, num):
        for i in range(9):
            if self.board[i][col] == num:
                return False
        return True

    # Check 3x3 box whether a number is used
    def innerbox_is_safe(self, row, col, num):
        for i in range(3):
            for j in range(3):
                if self.board[row + i][col + j] == num:
                    return False
        return True

    def safe_to_fill(self, row, col, num):
        return self.row_is_safe(row, num) and self.col_is_safe(col, num) and self.innerbox_is_safe(row - row % 3,
                                                                                                   col - col % 3,
                                                                                                   num)

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return [i, j]
        return None

    def find_list_empty(self):
        for row in range(self.PUZZLE_SIZE):
            for col in range(self.PUZZLE_SIZE):
                if self.board[row][col] == 0:
                    self.list_empty.append((row, col))

    def backtrack_search_cells(self, screen, cell_index):
        if cell_index == len(self.list_empty):
            return True

        cell_row, cell_col = self.list_empty[cell_index]
        for num in range(1, self.PUZZLE_SIZE + 1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if self.safe_to_fill(cell_row, cell_col, num):
                self.board[cell_row][cell_col] = num
                value = self.font.render(str(num), True, self.COLOR_BLACK)
                screen.blit(value, ((cell_col + 1) * 50 + 15, (cell_row + 1) * 50))
                pygame.display.update()
                pygame.time.delay(25)

                if self.backtrack_search_cells(screen, cell_index + 1) is True:
                    return True

                self.board[cell_row][cell_col] = 0
                pygame.draw.rect(screen, self.COLOR_WHITE,
                                 ((cell_col + 1) * 50 + self.BUFFER, (cell_row + 1) * 50 + self.BUFFER,
                                  50 - 2 * self.BUFFER,
                                  50 - 2 * self.BUFFER))
                pygame.display.update()

        return False

    def solve(self, screen):
        self.find_list_empty()
        return self.backtrack_search_cells(screen, 0)

    def clear(self):
        self.original_board = [[0] * self.PUZZLE_SIZE for _ in range(self.PUZZLE_SIZE)]
        self.board = [[0] * self.PUZZLE_SIZE for _ in range(self.PUZZLE_SIZE)]
