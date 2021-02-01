import re


class Node:
    def __init__(self, position, numericDomain):
        self.position = position
        self.numericDomain = numericDomain
        if len(numericDomain) == 1:
            self.hasValue = True
        else:
            self.hasValue = False


    def func(self):
        print("infrmations: ")
        print("X Y ", self.position)
        print("value: ", self.numericDomain)
        print("hase value: ", self.hasValue)


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
    rowCounter = 0
    columnCounter = 0
    for row in sudokuTable:
        for column in row:
            match = re.findall("\d", column)
            if match:
                num = 0
                for k in range(len(match)):
                    num = num*10 + int(match[k])
                numericSudoku[rowCounter][columnCounter] = num
            else:
                numericSudoku[rowCounter][columnCounter] = "-"
            columnCounter += 1
        columnCounter = 0
        rowCounter += 1

    return numericSudoku


def NodeMaker(numericSudoku):
    nodes = []
    print(nodes)
    i = j = 0
    for row in numericSudoku:
        for column in row:
            if column == '-':
                domain = [i+1 for i in range(len(numericSudoku))]
            else:
                domain = [column]
            nodes.append(Node((i, j), domain))
            print("i j: ", i, " ", j)
            print("domain: ", domain)
            print("has value: ", nodes[i*len(numericSudoku) + j].hasValue)
            j += 1
        j = 0
        i += 1


def main():
    numbers, colors, sudokuTable = extractInputFile("2DArray.txt")
    colorSize, TableSize = numbers
    print(colorSize, TableSize)
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
    NodeMaker(numericSudoku)

main()