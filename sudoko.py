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
        print("informations: ")
        print("X Y ", self.position)
        print("value: ", self.numericDomain)
        print("has value: ", self.hasValue)

    def neighbors(self):
        # print("X: ", self.position[0], " Y: ", self.position[1])
        rowNeighbors = []
        columnNeighbors = []
        for i in range(_tableSize):
            if i != self.position[0]:
                neighbor = (i, self.position[1])
                rowNeighbors.append(neighbor)
            if i != self.position[1]:
                neighbor = (self.position[0], i)
                columnNeighbors.append(neighbor)
        print("Row neighbors: ")
        for n in rowNeighbors:
            print(n)
        print("column neighbors: ")
        for n in columnNeighbors:
            print(n)
        return rowNeighbors, columnNeighbors

    def isNeighbor(self):
        rowNeighbors, columnNeighbors = self.neighbors()
        for row in rowNeighbors:
            print("row: ", row)


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


def numericSudokuMaker(sudokuTable):
    numericSudoku = [[0 for i in range(_tableSize)] for j in range(_tableSize)]
    rowCounter = 0
    columnCounter = 0
    for row in sudokuTable:
        for column in row:
            match = re.findall("\d", column)
            if match:
                num = 0
                for k in range(len(match)):
                    num = num * 10 + int(match[k])
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
                domain = [i + 1 for i in range(_tableSize)]
            else:
                domain = [column]
            nodes.append(Node((i, j), domain))
            # print("i j: ", i, " ", j)
            # print("domain: ", domain)
            # print("has value: ", nodes[i * len(numericSudoku) + j].hasValue)
            j += 1
        j = 0
        i += 1
    return nodes


def displaySudokuTable(_table):
    for row in _table:
        for column in row:
            print(column, end=" ")
        print()


def main():
    global _tableSize
    numbers, colors, sudokuTable = extractInputFile("2DArray.txt")
    colorSize, _tableSize = numbers
    print(colorSize, _tableSize)
    print(colors)
    displaySudokuTable(sudokuTable)
    numericSudoku = numericSudokuMaker(sudokuTable)
    displaySudokuTable(numericSudoku)
    nodes = NodeMaker(numericSudoku)
    # nodes[5].neighbors(tableSize)
    nodes[5].isNeighbor()


main()
