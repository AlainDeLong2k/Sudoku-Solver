import pygame
from Board import Board
from Box import Box


class Game:
    PUZZLE_SIZE = 9
    COLOR_BLACK = (0, 0, 0)

    def __init__(self, width, height):
        self.board = Board(40)
        self.row = self.col = 9
        self.boxes = [[Box(self.board.board[i][j], i, j) for j in range(self.PUZZLE_SIZE)] for i in
                      range(self.PUZZLE_SIZE)]
        self.width = width
        self.height = height
        self.gap = self.width // 10
        self.selected = None

    def place(self, val):
        if self.selected is None:
            return

        row, col = self.selected
        if self.board.original_board[row][col] == 0:
            self.boxes[row][col].set(val)
            self.board.board[row][col] = val

    def draw(self, screen):
        for i in range(self.row + 1):
            if i % 3 == 0:  # Draw thicker border every 3x3 box
                thick = 4
            else:
                thick = 2
            pygame.draw.line(screen, self.COLOR_BLACK, (self.gap, self.gap + i * self.gap),
                             (self.width, self.gap + i * self.gap),
                             thick)  # Draw horizontal line
            pygame.draw.line(screen, self.COLOR_BLACK, (self.gap + i * self.gap, self.gap),
                             (self.gap + i * self.gap, self.height),
                             thick)  # Draw vertical line

        for i in range(9):
            for j in range(9):
                original = self.board.original_board[i][j] != 0
                self.boxes[i][j].draw(screen, original)

    def select(self, row, col):
        # Reset other box selected status
        for i in range(self.PUZZLE_SIZE):
            for j in range(self.PUZZLE_SIZE):
                self.boxes[i][j].selected = False

        self.selected = None
        row, col = int(row - 1), int(col - 1)
        if 0 <= row < self.PUZZLE_SIZE and 0 <= col < self.PUZZLE_SIZE:
            if self.board.original_board[row][col] == 0:
                self.boxes[row][col].selected = True  # Mark current clicked box as selected
                self.selected = (row, col)

    def clear(self):
        if self.selected is None:
            return
        row, col = self.selected

        # Clear selected box attributes
        if self.board.original_board[row][col] == 0:
            self.boxes[row][col].set(0)
            self.board.board[row][col] = 0

    def click(self, pos):
        x = pos[0] // self.gap
        y = pos[1] // self.gap
        return y, x

    def check_empty_box(self):
        for i in range(self.PUZZLE_SIZE):
            for j in range(self.PUZZLE_SIZE):
                if self.boxes[i][j] == 0:
                    return True
        return False

    # def check_answer(self):
    # self.board.solve()  # To solve current board
    # for i in range(9):
    #     for j in range(9):
    #         if self.board.board[i][j] != self.boxes[i][j].value:
    #             return False
    # return True
    def solve(self, screen):
        return self.board.solve(screen)

    def input_puzzle(self):
        self.board.clear()
        self.boxes = [[Box(self.board.board[i][j], i, j) for j in range(self.PUZZLE_SIZE)] for i in
                      range(self.PUZZLE_SIZE)]
