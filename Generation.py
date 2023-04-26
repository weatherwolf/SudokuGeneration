import copy
from random import choice

# difficulty means the maximum amount of empty cells in the sudoku puzzle
difficulty = 60

# generating the empty sudoku and some useful lists
grid = []
for i in range(9):
    grid.append([0,0,0,0,0,0,0,0,0])

intList = [1,2,3,4,5,6,7,8,9]
cellList = []
for i in range(80):
    cellList.append(i)


# make a 3x3 box with a given row and col value which does not including the value itself
def box(row, col, sudoku) -> list:
    boxList = []
    boxRow = 0
    boxCol = 0
    while row >= 3:
        boxRow += 1
        row -= 3
    while col >= 3:
        boxCol += 1
        col -= 3
    for i in range(3*boxRow, 3*boxRow+3):
        for j in range(3*boxCol, 3*boxCol+3):
            boxList.append(sudoku[i][j])
    return boxList

# check for 3 different constraints. Each cell may contain a number from 1 to 9
# each numer can only occur once in each row, column and box.
def constraints(value, row, col, sudoku) -> bool:
    if value < 0 or value >= 10:
        raise TypeError("Value is not between 1-9")
    # check if value in row or column
    for i in range(9):
        if value == sudoku[row][i] and i != col:
            return False
        elif value == sudoku[i][col] and i != row:
            return False
    # check if value in box
    tempBox = box(row, col, sudoku)
    if value in tempBox:
        return False
    return True

# using a depth first search to create a full working sudoku
def SudokuGenerationSolved(sudoku, counter, notVisited) -> list:
    if counter == 81:
        return sudoku
    else:
        tempSudoku = copy.deepcopy(sudoku)
        row = counter//9
        col = counter%9
        while notVisited:
            value = choice(notVisited)
            notVisited.remove(value)
            tempSudoku[row][col] = value
            if constraints(value, row, col, sudoku):
                result = SudokuGenerationSolved(tempSudoku, counter+1, copy.deepcopy(intList))
                if result is not None:  # If a solution is found, return it
                    return result
        return None

# creates a sudoku with a unique solution, which is done by SudokuSolver.
def SudokuGenerationPuzzle(sudoku, emptyCells, counter) -> list:
    tempCellList = copy.deepcopy(cellList)
    for emptyCell in emptyCells:
        tempCellList.remove(emptyCell)
    while counter <= difficulty and tempCellList:
        cell = choice(tempCellList)
        tempCellList.remove(cell)
        row = cell//9
        col = cell%9
        tempValue = sudoku[row][col]
        sudoku[row][col] = 0
        tempEmptyCells = copy.copy(emptyCells)
        tempEmptyCells.append(cell)
        result = SudokuPuzzleSolver(sudoku, tempEmptyCells, 0)
        if result <= 1:
            return SudokuGenerationPuzzle(sudoku, tempEmptyCells, counter+1)
        sudoku[row][col] = tempValue
    return sudoku

# backtracking solver used to generate a unique sudoku puzzle from a solved sukodu
def SudokuPuzzleSolver(sudoku, emptyCells, counter) -> int:
    if not emptyCells:
        counter += 1 
    else:
        cell = emptyCells[0]
        emptyCells = emptyCells[1:]
        row = cell//9
        col = cell%9 
        for value in range(1,10):
            if constraints(value, row, col, sudoku):
                sudoku[row][col] = value
                counter += SudokuPuzzleSolver(sudoku, emptyCells, counter)
            sudoku[row][col] = 0
    return counter

# backtracking solver that can you used to solve sudoku puzzles 
def fullSudokuSolver(sudoku, emptyCells) -> list:
    if not emptyCells:
        return sudoku
    else:
        cell = emptyCells[0]
        emptyCells = emptyCells[1:]  # use slicing to remove first element
        row, col = divmod(cell,9)
        for value in range(1,10):
            if constraints(value, row, col, sudoku):
                sudoku[row][col] = value
                result = fullSudokuSolver(sudoku, emptyCells)  # store the result of recursive call
                if result is not None:  # check if a solution was found
                    return result
                else:
                    sudoku[row][col] = 0


output = SudokuGenerationSolved(grid, 0, copy.deepcopy(intList))
completedOutput = SudokuGenerationPuzzle(copy.deepcopy(output), [], 0)
emptyCellsOutput = []
for i in range(81):
    row, col = divmod(i,9)
    if completedOutput[row][col] == 0:
        emptyCellsOutput.append(i)
print('Done creating sudoku puzzle')

# Used for testing the fullSudokuSolver function
solvedOutput = fullSudokuSolver(copy.deepcopy(completedOutput), emptyCellsOutput)

