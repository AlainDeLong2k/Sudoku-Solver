import random
import sudoku_ant
from Board import Board
from copy import deepcopy


class SudokuAntSystem:
    def __init__(self, numAnts, q0, rho, pher0, bestEvap):
        self.numAnts = numAnts
        self.q0 = q0
        self.rho = rho
        self.pher0 = pher0
        self.bestEvap = bestEvap
        self.bestSol = None
        self.bestPher = 0.0
        self.bestVal = -1
        self.antList = [sudoku_ant.SudokuAnt(self) for _ in range(numAnts)]
        # self.randomDist = [random.uniform(0.0, 1.0) for _ in range(numAnts)]
        self.randomGen = random.Random()
        self.pher = []
        self.numCells = 0

    def initPheromone(self, numCells, valuesPerCell):
        self.numCells = numCells
        self.pher = [[self.pher0] * valuesPerCell for _ in range(numCells)]

    def clearPheromone(self):
        self.pher = []

    def updatePheromone(self):
        for i in range(self.numCells):
            row, col = i // 9, i % 9
            if self.bestSol.board[row][col] > 0:
                self.pher[i][self.bestSol.board[row][col] - 1] = self.pher[i][self.bestSol.board[row][col] - 1] * (
                        1 - self.rho) + self.rho * self.bestPher

    def pherAdd(self, cellsFilled):
        if self.numCells == cellsFilled:
            return 100000000000000000
        return self.numCells * 1.0 / (self.numCells - cellsFilled)

    def getSolution(self):
        return self.bestSol

    def get_q0(self):
        return self.q0

    def get_random(self):
        # print(self.randomDist)
        # rnd = random.randint(0, 9)
        # return self.randomDist[rnd]
        return self.randomGen.uniform(0.0, 1.0)
        # rnd = self.randomGen.uniform(0.0, 1.0)
        # print(rnd)
        # return rnd

    def getPher(self, i, j):
        return self.pher[i][j]

    def updateLocalPheromone(self, iCell, iChoice):
        self.pher[iCell][iChoice] = self.pher[iCell][iChoice] * 0.9 + self.pher0 * 0.1

    def solve(self, board):
        iter = 0
        solved = False
        bestPher = 0
        curBestAnt = 0
        self.initPheromone(81, 9)
        while solved is False:
            for ant in self.antList:
                rnd = random.randint(0, 80)
                ant.init_solution(board, rnd)

            for i in range(81):
                for ant in self.antList:
                    ant.step_solution()

            antBest = 0
            bestVal = 0
            for ant in self.antList:
                if ant.numCellsFilled() > bestVal:
                    bestVal = ant.numCellsFilled()
                    antBest = ant

            pherToAdd = self.pherAdd(bestVal)
            if pherToAdd > bestPher:
                self.bestSol = deepcopy(antBest.sol)
                bestPher = pherToAdd
                if bestVal == self.numCells:
                    solved = True
            self.updatePheromone()
            bestPher *= (1.0 - self.bestEvap)
            iter += 1
            if iter % 100 == 0:
                break

        if solved is True:
            print('Iteration:', iter)
        self.clearPheromone()
        return solved

# def main1():
#     t = SudokuAntSystem(10, 1, 1, 1, 1)
#     print(t.get_random())
#
#
# if __name__ == '__main__':
#     main1()
