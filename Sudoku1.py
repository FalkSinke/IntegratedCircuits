from __future__ import print_function
#test comment
def readSudoku():
    with open("puzzle1.sudoku") as f:
        sudoku = []
        for line in f.read().split():
            sudoku.append([int(e) for e in line.split(",")])
    return sudoku

def execute():
    s = readSudoku()
    printSudoku(s)
    while not checkComplete(s):
        if not updateNumbers(s):
            print ("infinite loop, stopped")
            break
    printSudoku(s)

# prints the whole sudoku
def printSudoku(sudoku):
    print("* - - - * - - - * - - - *")
    for j in range (9):
        print('|', end='')
        print(' ', end='')
        for i in range (9):
            print(sudoku[j][i], end=' ')
            if (i%3 == 2):
                print('|', end=' ')
        print('')
        if (j%3 == 2):
            print("* - - - * - - - * - - - *")

# checks how many rows, columns and blocks are completed,
# gives completed value to
def checkComplete(sudoku):
    for i in range (9):
        for k in range (1, 10):
            if not numInRow(sudoku, i, k) or not numInColumn(sudoku, i, k):
                return False
        for j in range (9):
            if i%3 == 0 and j%3 == 0:
                for k in range (1, 10):
                    if not numInBlock(sudoku, i, j, k):
                        return False
    print("Sudoku complete, well done!")
    return True

# checking function if a number is in the block of given location
def numInBlock(sudoku, row, column, number):
    row -= row % 3
    column -= column % 3
    for i in range(column, column + 3):
        for j in range(row, row + 3):
            if sudoku[j][i] == number:
                return True
    return False

# checks if number is in given row
def numInRow(sudoku, row, number):
    return any(sudoku[row][i] == number for i in range(9))
    #for i in range (0,9):
    #    if sudoku[row][i] == number:
    #        return True
    #return False

# checks if number is in given column
def numInColumn(sudoku, column, number):
    for i in range (9):
        if sudoku[i][column] == number:
            return True
    return False

# iterates through whole sudoku, updates each value where only 1 number
# possible
def updateNumbers(sudoku):
    inProgress = 0
    for row in range (9):
        for column in range (9):
            if(isdigit(sudoku[row][column]))
                if sudoku[row][column] == 0:
                    numbers = []
                    for i in range (1,10):
                        if not (numInRow(sudoku, row,i) or numInBlock(sudoku,\
                                row,column,i) or numInColumn(sudoku, column,i)):
                            numbers.append(i)
                    if len(numbers) == 1:
                        sudoku[row][column] = numbers[0]
                        inProgress = 1
                    else:
                        sudoku[row][column] = numbers
                        inProgress = 1
            else:
                for i in sudoku[row][column]:
                    if (numInRow(sudoku, row,i) or numInBlock(sudoku,\
                                row,column,i) or numInColumn(sudoku, column,i)):
                        sudoku[row][column].remove(i)
                        inProgress = 1
                    if len(sudoku[row][column] == 1):
                        sudoku[row][column] = sudoku[row][column][0]
                        inProgress = 1
    return inProgress == 1

execute()

#test commit122
