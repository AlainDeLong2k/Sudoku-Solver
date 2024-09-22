import pyautogui
from sudoku_ant_system import SudokuAntSystem
from board_sudoku import BoardSudoku


def main():
    nAnts = 10
    q0 = 0.9
    rho = 0.9
    evap = 0.005

    board = [
        [0, 0, 7, 0, 5, 2, 0, 0, 6],
        [0, 0, 2, 7, 8, 0, 0, 0, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 5, 4, 3, 1, 0, 0],
        [0, 7, 3, 1, 9, 0, 0, 0, 0],
        [0, 0, 0, 6, 2, 0, 0, 0, 0],
        [0, 8, 5, 9, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 6, 1, 8, 0, 0],
        [2, 0, 9, 0, 0, 5, 0, 6, 7]
    ]

    b = BoardSudoku(board)

    solver = SudokuAntSystem(nAnts, q0, rho, 1.0 / 81, evap)
    success = solver.solve(b)

    if success is True:
        print('aaaaaaaaaaaaa')
        sol = solver.getSolution()
        print(sol.board)
        for line in sol.board:
            print(line)


if __name__ == '__main__':
    main()
