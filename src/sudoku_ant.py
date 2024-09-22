# import sudoku_ant_system
import pygame
from Board import Board
from copy import deepcopy
from board_sudoku import BoardSudoku


class SudokuAnt:
    def __init__(self, parent):
        self.sol: BoardSudoku = None
        self.iCell = 0
        self.parent = parent
        self.failCells = 0
        self.roulette = []
        self.roulette_vals = []

    def init_solution(self, puzzle: BoardSudoku, start_cell):
        self.sol = deepcopy(puzzle)
        self.iCell = start_cell
        self.failCells = 0
        self.roulette = [0 for _ in range(9)]
        self.roulette_vals = [0 for _ in range(9)]

    def step_solution(self):
        if self.sol.cell_empty(self.iCell) is True:
            self.failCells += 1
        elif self.sol.cell_fixed(self.iCell) is False:
            if self.parent.get_random() > self.parent.get_q0():
                best = 0
                maxPher = -1.0
                for choice in self.sol.listCells[self.iCell]:
                    if self.parent.getPher(self.iCell, choice - 1) > maxPher:
                        maxPher = self.parent.getPher(self.iCell, choice - 1)
                        best = choice

                self.sol.set_cell(self.iCell, best)
                self.parent.updateLocalPheromone(self.iCell, best - 1)
            else:
                totPher = 0.0
                numChoices = 0
                for choice in self.sol.listCells[self.iCell]:
                    self.roulette[numChoices] = totPher + self.parent.getPher(self.iCell, choice - 1)
                    totPher = self.roulette[numChoices]
                    self.roulette_vals[numChoices] = choice
                    numChoices += 1

                rouletteVal = totPher * self.parent.get_random()
                for i in range(numChoices):
                    if self.roulette[i] > rouletteVal:
                        self.sol.set_cell(self.iCell, self.roulette_vals[i])
                        self.parent.updateLocalPheromone(self.iCell, self.roulette_vals[i] - 1)
                        break
        self.iCell += 1
        if self.iCell == 81:
            self.iCell = 0

    def numCellsFilled(self):
        return 81 - self.failCells


# def main():
#     t = SudokuAnt(None)
#     t.init_solution(None, 0)
#     print(t.roulette)
#     print(t.roulette_vals)
#
#
# main()
