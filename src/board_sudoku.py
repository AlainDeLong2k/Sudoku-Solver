from Board import Board
from copy import deepcopy


class BoardSudoku:
    def __init__(self, board):
        self.board = deepcopy(board)
        # self.board = [
        #     [0, 6, 0, 0, 0, 0, 5, 0, 2],
        #     [0, 3, 0, 0, 0, 7, 0, 0, 0],
        #     [0, 2, 0, 3, 0, 6, 0, 0, 7],
        #     [8, 7, 3, 0, 2, 1, 4, 5, 0],
        #     [9, 4, 0, 5, 0, 0, 0, 0, 0],
        #     [0, 1, 0, 0, 0, 4, 0, 0, 0],
        #     [0, 0, 0, 0, 9, 5, 0, 0, 4],
        #     [3, 9, 4, 8, 1, 0, 0, 7, 5],
        #     [0, 5, 1, 0, 6, 3, 0, 9, 8]
        # ]
        self.listCells = []
        self.listFixed = []
        for row in range(9):
            for col in range(9):
                if self.board[row][col] > 0:
                    self.listFixed.append((row, col))
                    self.listCells.append([self.board[row][col]])
                else:
                    self.listCells.append([i + 1 for i in range(9)])

        # print('Before')
        # for line in self.listCells:
        #     print(line, end='')
        # print('After-------------------------------')
        # for i in range(81):
        #     if i % 9 == 0:
        #         print()
        #     print(self.listCells[i], end='')
        for i in range(len(self.listFixed)):
            self.propagation(self.listFixed[i][0], self.listFixed[i][1])
        # for i in range(81):
        #     if i % 9 == 0:
        #         print()
        #     print(self.listCells[i], end=' ')

    def propagation(self, row, col):
        # print(row, col)
        pos = row * 9 + col
        for i in range(9):
            if row * 9 + i != pos:
                if self.board[row][col] in self.listCells[row * 9 + i]:
                    self.listCells[row * 9 + i].remove(self.board[row][col])
                    # self.propagation(row, i)
                    if len(self.listCells[row * 9 + i]) == 1:
                        self.board[row][i] = self.listCells[row * 9 + i][0]
                        self.propagation(row, i)

            if i * 9 + col != pos:
                if self.board[row][col] in self.listCells[i * 9 + col]:
                    self.listCells[i * 9 + col].remove(self.board[row][col])
                    # self.propagation(i, col)
                    if len(self.listCells[i * 9 + col]) == 1:
                        self.board[i][col] = self.listCells[i * 9 + col][0]
                        self.propagation(i, col)

        box_row = row // 3 * 3
        box_col = col // 3 * 3
        for i in range(3):
            for j in range(3):
                if (box_row + i) * 9 + (box_col + j) != pos:
                    if self.board[row][col] in self.listCells[(box_row + i) * 9 + (box_col + j)]:
                        self.listCells[(box_row + i) * 9 + (box_col + j)].remove(self.board[row][col])
                        # self.propagation(box_row + i, box_col + j)
                        if len(self.listCells[(box_row + i) * 9 + (box_col + j)]) == 1:
                            self.board[box_row + i][box_col + j] = self.listCells[(box_row + i) * 9 + (box_col + j)][0]
                            self.propagation(box_row + i, box_col + j)

    def set_cell(self, iCell, cell):
        self.board[iCell // 9][iCell % 9] = cell
        self.propagation(iCell // 9, iCell % 9)

    def cell_empty(self, iCell):
        return len(self.listCells[iCell]) == 0

    def cell_fixed(self, iCell):
        return len(self.listCells[iCell]) == 1

# def main():
#     t = BoardSudoku()
#     # for line in t.board:
#     #     print(line)
#     # print(t.listFixed)
#     # for line in t.listCells:
#     #     print(line)
#
#
# main()
