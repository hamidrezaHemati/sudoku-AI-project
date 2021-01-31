import re


def extractInputFile(fileName):
    with open(fileName) as f:
        line = f.readline()
        numbers = [int(s) for s in line.split() if s.isdigit()]
        tableSize = numbers[1]
        colors = f.readline().split()
        sudokuTable = [[0 for i in range(tableSize)] for j in range(tableSize)]
        for i in range(tableSize):
            sudokuTable[i] = f.readline().split()

    return numbers, colors, sudokuTable

def numericSudokuMaker(sudokuTable, size):
    numericSudoku = [[0 for i in range(size)] for j in range(size)]
    rowCounter=0
    columnCounter=0
    for row in sudokuTable:
        for column in row:
            match = re.findall("\d", column)
            if match:
                num = 0
                for k in range(len(match)):
                    num = num*10 + int(match[k])
                numericSudoku[rowCounter][columnCounter] = num
            else:
                numericSudoku[rowCounter][columnCounter] = 0
            columnCounter+=1
        columnCounter=0
        rowCounter+=1

    return numericSudoku



def main():
    numbers, colors, sudokuTable = extractInputFile("2DArray.txt")
    clolorSize, TableSize = numbers
    print(clolorSize, TableSize)
    print(colors)
    for row in sudokuTable:
        for column in row:
            print(column, end=" ")
        print()
    numericSudoku = numericSudokuMaker(sudokuTable, numbers[1])
    for row in numericSudoku:
        for column in row:
            print(column, end=" ")
        print()

main()