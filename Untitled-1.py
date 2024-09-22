from tkinter import *


root = Tk()
root.geometry('275x283')
class Solver():
    def __init__(self):
        self.setZero()
        self.startSolution()
        
    def setZero(self):
        for i in range(9):
            for j in range(9):
                if board[i][j].get() not in ['1','2','3','4','5','6','7','8','9']:
                    board[i][j].set(0)
                    
    def startSolution(self,i=0,j=0):
        i,j=self.findEmptyCells(i,j)
        if i==-1 or j==-1: 
            return True
        for e in range(1,10):
            if self.checkValidity(i,j,e):
                board[i][j].set(e)
                if self.startSolution(i,j): 
                    return True
                board[i][j].set(0)
        return False
    def findEmptyCells(self,i,j):
        for x in range (0,9):
            for y in range (0,9):
                if board[x][y].get() == '0':
                    return x,y
        return -1,-1
    def checkValidity(self,i,j,e):
        
        for x in range (9):
            if board[i][x].get()==str(e): 
                return False
        
        for x in range (9):
            if board[x][j].get()==str(e): 
                return False
        
        boxX=3*int((i/3))
        boxY=3*int((j/3))
        for x in range(boxX,boxX+3):
            for y in range(boxY,boxY+3):
                if board[x][y].get()==str(e):
                    return False
        return True
    
        
class GUI():
    
    # Set Title, Grid and Menu
    def __init__(self, master):
        
        # Title and settings
        self.master = master
        master.title("Sudoku Solver")
        font = ('Arial', 18)
        color = 'white'
        px, py = 0, 0

        # Front-end Grid
        self.__table = []
        for i in range(1,10):
            self.__table += [[0,0,0,0,0,0,0,0,0]]

        for i in range(0,9):
            for j in range(0,9):
                
                if (i < 3 or i > 5) and (j < 3 or j > 5):
                    color = 'gray'
                elif i in [3,4,5] and j in [3,4,5]:
                    color = 'gray'
                else:
                    color = 'white'

                self.__table[i][j] = Entry(master, width = 2, font = font, bg = color, cursor = 'arrow', borderwidth = 0,
                                          highlightcolor = 'yellow', highlightthickness = 1, highlightbackground = 'black',
                                          textvar = board[i][j])
                self.__table[i][j].bind('<Motion>', self.correctGrid)
                self.__table[i][j].bind('<FocusIn>', self.correctGrid)
                self.__table[i][j].bind('<Button-1>', self.correctGrid)
                self.__table[i][j].grid(row=i, column=j)


        # Front-End Menu
        menu = Menu(master)
        master.config(menu = menu)

        file = Menu(menu)
        menu.add_cascade(label = 'File', menu = file)
        file.add_command(label = 'Exit', command = master.quit)
        file.add_command(label = 'Solve', command = self.solveInput)
        file.add_command(label = 'Clear', command = self.clearAll)

    
    # Correct the Grid if inputs are incorrect
    def correctGrid(self, event):
        for i in range(9):
            for j in range(9):
                if board[i][j].get() == '':
                    continue
                if len(board[i][j].get()) > 1 or board[i][j].get() not in ['1','2','3','4','5','6','7','8','9']:
                    board[i][j].set('')


    # Clear the Grid
    def clearAll(self):
        for i in range(9):
            for j in range(9):
                board[i][j].set('')


    # Calls the class SolveSudoku
    def solveInput(self):
        solution = Solver()

        
        

# Global Matrix where are stored the numbers
board = []
for i in range(1,10):
    board += [[0,0,0,0,0,0,0,0,0]]
for i in range(0,9):
    for j in range(0,9):
        board[i][j] = StringVar(root)

app = GUI(root)
root.mainloop()