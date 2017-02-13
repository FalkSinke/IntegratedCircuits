from __future__ import print_function

with open("puzzle1.sudoku") as f:
    sudoku = []
    for line in f.read().split():
        sudoku.append(line.split(','))

for i in range (0, 9):
    for j in range (0, 9):
        sudoku[i][j] = int(sudoku[i][j])

#prints the whole sudoku
def printSudoku():
    print("* - - - * - - - * - - - *")
    for j in range (0, 9):
        print('|', end='')
        print(' ', end='')
        for i in range (0,9):
            print(sudoku[j][i], end=' ')
            if (i%3 == 2):
                print('|', end=' ')
        print('')
        if (j%3 == 2):
            print("* - - - * - - - * - - - *")

#checks if specific row is complete
def checkRow(rownumber):
    checkcount = 0;
    for i in range (1,10):
        if i in sudoku[rownumber]:
            checkcount = checkcount + 1;
    if checkcount == 9:
        return 1
    else:
        return 0
 
#checks if specific column is complete
def checkColumn(columnNumber):
    column = []
    for i in range (0,9):
        column.append(sudoku[i][columnNumber])
    checkcount = 0;
    for i in range(1, 10):
        if i in column:
            checkcount += 1
    if checkcount == 9:
        return 1
    else:
        return 0

#insert left upper corner of block
#take in account, left upper corner is 0,0
def checkBlock(column, row):
    numbers = []
    for i in range (column, column + 3):
        for j in range (row, row + 3):
            numbers.append(sudoku[j][i])
    checkcount = 0;
    for i in range(1, 10):
        if i in numbers:
            checkcount += 1
    if checkcount == 9:
        return 1
    else:
        return 0

#checks how many rows, columns and blocks are completed,
# gives completed value to
def checkComplete():
    rows = 0
    columns = 0
    blocks = 0

    for i in range (0,9):
        rows += checkRow(i)
        columns += checkColumn(1)
        for j in range (0,9):
            if i%3 == 0 and j%3==0:
                blocks += checkBlock(i,j)
    #print(" ")
    if rows + columns + blocks == 27:
        print("You completed the sudoku!")
        return True
    #else:
    #    print("So far completed:")
    #    print("Columns:", columns)
    #    print("Rows:", columns)
    #    print("Blocks:", blocks)
    #    return False

#checking function if a number is in the block of given location
def numInBlock(row,column,number):
    row -= row % 3
    column -= column % 3
    for i in range(column, column + 3):
        for j in range(row, row + 3):
            if sudoku[j][i] == number:
                #print (number, "in row", j, "column", i)
                return True
    return False

#checks if number is in given row
def numInRow(row, number):
    for i in range (0,9):
        if sudoku[row][i] == number:
            #print (number, "in row", row)
            return True
    return False

#checks if number is in given column
def numInColumn(column, number):
    for i in range (0,9):
        if sudoku[i][column] == number:
            #print (number, "in column", column)
            return True
    return False

def updateNumbers():
    inProgress = 0
    for row in range (0,9):
        for column in range (0,9):
            if sudoku[row][column] == 0:
                numbers = []
                for i in range (1,10):
                    if not (numInRow(row,i) or numInBlock(row,column,i) or numInColumn(column,i)):
                        numbers.append(i)
                if len(numbers) == 1:
                    #print (numbers[0], "row", row, "column", column)
                    sudoku[row][column] = numbers[0]
                    inProgress = 1;
    if inProgress == 1:
        return True
    else:
        return False

#printSudoku()
while not checkComplete():
    if not updateNumbers():
        print ("infinite loop, stopped")
        break
printSudoku()
#checkComplete()
