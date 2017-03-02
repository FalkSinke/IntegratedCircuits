from __future__ import print_function
import math
import copy

# Falk Sinke, Lucas Fijen en Claartje Barkhof

# Reads the sudoku text, and translates it
# into a 2D list.
def readSudoku(filename):
    with open(filename) as f:
        sudoku = []
        for line in f.read().split():
            sudoku.append([int(e) for e in line.split(",")])
    return sudoku

# iterates through the 6 puzzles:
def runMultipleSudokus():
        execute("puzzle1.sudoku")
        execute("puzzle2.sudoku")
        execute("puzzle3.sudoku")
        execute("puzzle4.sudoku")
        execute("puzzle5.sudoku")
        execute("puzzle6.sudoku")

# Tries to solve the sudoku the easy way (updateNumbers)
# and completes it (if necessary) with a pruning depth-first
# algorithm (solveSudoku).
def execute(filename):
    s = readSudoku(filename)
    print(" ")
    print("Unsolved sudoku ", filename)
    printSudoku(s)
    initialisePossibilities(s)
    while not checkComplete(s):
        if not updatePossibilities(s):
            if solveSudoku(s):
                break
            else:
                print("This sudoku is unsolvable.")
            break
    if checkComplete(s):
        print("The completed sudoku is: ")
        printSudoku(s)

def printHorizontalDevide(sudoku, blocksize):
    for j in range (len(sudoku)):
        if (j % blocksize == 0):
            print("* ", end='')
        print("- ", end='')
    print("*")

# prints the whole sudoku
def printSudoku(sudoku):
    blocksize = int(math.sqrt(len(sudoku)))
    printHorizontalDevide(sudoku, blocksize)
    for j in range (len(sudoku)):
        print('|', end='')
        print(' ', end='')
        for i in range (len(sudoku[0])):
            print(sudoku[j][i], end=' ')
            if (i % blocksize == 2):
                print('|', end=' ')
        print('')
        if (j % blocksize == 2):
            printHorizontalDevide(sudoku, blocksize)

# checks how many rows, columns and blocks are completed,
# gives completed value to
def checkComplete(sudoku):
    blocksize = int(math.sqrt(len(sudoku)))
    for i in range (len(sudoku)):
        for k in range (1, len(sudoku) + 1):
            if not numInRow(sudoku, i, k) or not numInColumn(sudoku, i, k):
                return False
        for j in range (len(sudoku[0])):
            if i%blocksize == 0 and j%blocksize == 0:
                for k in range (1, len(sudoku) + 1):
                    if not numInBlock(sudoku, i, j, k):
                        return False
    return True

# checking function if a number is in the block of given location
def numInBlock(sudoku, row, column, number):
    blocksize = int(math.sqrt(len(sudoku)))
    row -= row % blocksize
    column -= column % blocksize
    for i in range(column, column + blocksize):
        for j in range(row, row + blocksize):
            if sudoku[j][i] == number:
                return True
    return False

# checks if number is in given row
def numInRow(sudoku, row, number):
    for i in range (len(sudoku)):
        if sudoku[row][i] == number:
            return True
    return False

# checks if number is in given column
def numInColumn(sudoku, column, number):
    for i in range (len(sudoku[0])):
        if sudoku[i][column] == number:
            return True
    return False

# Fills in all numbers that are certain and initialises
# lists of possibilities
def initialisePossibilities(sudoku):
    for row in range (len(sudoku)):
        for column in range (len(sudoku[0])):
            if sudoku[row][column] == 0:
                numbers = []
                for i in range (1, len(sudoku) + 1):
                    if not (numInRow(sudoku, row,i) or numInBlock(sudoku,\
                            row,column,i) or numInColumn(sudoku, column,i)):
                        numbers.append(i)
                if len(numbers) == 1:
                    sudoku[row][column] = numbers[0]
                else:
                    sudoku[row][column] = numbers

# Updates lists of possibilities and return 0 if
# it can't update anymore.
def updatePossibilities(sudoku):
    inProgress = 0
    for row in range(len(sudoku)):
        for column in range(len(sudoku[0])):
            if isinstance(sudoku[row][column], list):
                for i in sudoku[row][column]:
                    if (    numInRow(sudoku, row, i) or numInBlock(sudoku, \
                            row, column, i) or numInColumn(sudoku, column, i)):
                        sudoku[row][column].remove(i)
                        inProgress = 1
                    if len(sudoku[row][column]) == 1:
                        sudoku[row][column] = sudoku[row][column][0]
                        inProgress = 1
    return inProgress == 1

# This code searches for the answer to the sudoku using depthfirst.
# It iterates through the possibilities inside the array.
# It uses pruning to prevent conflicting input, which decreases the possible
# answers drasticly.
# Returns a false if the predicate can't find an answer in this branch.
def solveSudoku(sudoku):
    if checkComplete(sudoku):
        print("The completed sudoku is: ")
        printSudoku(sudoku)
        return True
    for row in range(len(sudoku)):
        for column in range(len(sudoku[0])):
            if not isinstance(sudoku[row][column], int):
                sudokucopy = copy.deepcopy(sudoku)
                for i in sudoku[row][column]:
                    if not(numInRow(sudokucopy, row, i) or \
                            numInColumn(sudokucopy, column, i) or\
                            numInBlock(sudokucopy, row, column, i)):
                        sudokucopy[row][column] = i
                        if solveSudoku(sudokucopy):
                            return True
                return False

runMultipleSudokus()
