import pygame
import time
import pyautogui as pg
import util
from Game import Game
from board_sudoku import BoardSudoku
from sudoku_ant_system import SudokuAntSystem

SCREEN_HEIGHT, SCREEN_WIDTH = 550, 550
PUZZLE_HEIGHT, PUZZLE_WIDTH = 500, 500
COLOR_WHITE = (251, 247, 245)
COLOR_BLACK = (0, 0, 0)


def redraw_window(screen, board, current_time):
    screen.fill(COLOR_WHITE)
    font = pygame.font.SysFont('Comic Sans MS', 35)
    text = font.render("Time: " + util.format_time(current_time), True, COLOR_BLACK)
    screen.blit(text, (540 - 180, 500))  # Draw time on bottom right corner
    board.draw(screen)


def autofill_solution(solution):
    time.sleep(2)
    for row in range(9):
        for col in range(9):
            pg.press(str(solution[row][col]))
            pg.hotkey('right')
        pg.hotkey('down')
        for _ in range(8):
            pg.hotkey('left')


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sudoku")

    board = Game(PUZZLE_WIDTH, PUZZLE_HEIGHT)
    # t = BoardSudoku(board.board)
    # for line in t.board:
    #     print(line)
    # print(t.listFixed)
    # for line in t.listCells:
    #     print(line)

    nAnts = 10
    q0 = 0.9
    rho = 0.9
    evap = 0.005

    running = True
    start = time.time()

    while running:
        current_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])

            elif event.type == pygame.KEYDOWN:
                if util.get_key(event.key) is not None:
                    pressed = util.get_key(event.key)
                    board.place(pressed)

                elif event.key == pygame.K_SPACE:
                    help_str = "Press 1 - 9 to enter a number\n" \
                               "ENTER to solve the puzzle\n" \
                               "Press BACKSPACE to delete a number. Have fun!"
                    util.show_messagebox("Help", help_str)
                    board.input_puzzle()

                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    board.clear()

                elif event.key == pygame.K_RETURN:
                    puzzle = BoardSudoku(board.board.board)
                    solver = SudokuAntSystem(nAnts, q0, rho, 1.0 / 81, evap)
                    success = solver.solve(puzzle)
                    numIters = 0
                    start = time.time()
                    while success is False:
                        numIters += 100
                        solver = SudokuAntSystem(nAnts, q0, rho, 1.0 / 81, evap)
                        success = solver.solve(puzzle)
                    print('Estimated Iteration:', numIters)
                    current_time = round(time.time() - start)
                    end_str = "Ant Colony Optimization have solved this board in " + util.format_time(
                        current_time) + "\nPress OK to start a new game"
                    util.show_messagebox("Board completed!", end_str)
                    sol = solver.getSolution()
                    autofill_solution(sol.board)
                    for line in sol.board:
                        print(line)
                    for i in range(9):
                        for j in range(9):
                            board.boxes[i][j].value = sol.board[i][j]

                        start = time.time()
                        # board = Game(PUZZLE_WIDTH, PUZZLE_HEIGHT)

                    # start = time.time()
                    # if board.solve(screen):
                    #     current_time = round(time.time() - start)
                    #     end_str = "Backtracking Search have solved this board in " + util.format_time(current_time) + \
                    #               "\nPress OK to start a new game "
                    #     util.show_messagebox("Board completed!", end_str)
                    #     start = time.time()
                    #     board = Game(PUZZLE_WIDTH, PUZZLE_HEIGHT)

        redraw_window(screen, board, current_time)
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
