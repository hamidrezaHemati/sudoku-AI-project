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
        # print("Row neighbors: ")
        # for n in rowNeighbors:
        #     print(n)
        # print("column neighbors: ")
        # for n in columnNeighbors:
        #     print(n)
        return rowNeighbors, columnNeighbors

    def isNeighbor(self, neighborCoordinateToCheck):
        rowNeighbors, columnNeighbors = self.neighbors()
        for row in rowNeighbors:
            if row == neighborCoordinateToCheck:
                print("row: ",row)
                print("finded neighbor: ", neighborCoordinateToCheck)
                return True
            else:
                continue
        for column in columnNeighbors:
            if column == neighborCoordinateToCheck:
                print("column: ", column)
                print("finded neighbor: ", neighborCoordinateToCheck)
                return True
            else:
                continue
        return False


def degreeCalculator(node, nodes):
    rowNeighbors, columnNeighbors = node.neighbors()
    # print(rowNeighbors)
    # print(columnNeighbors)

    degree = len(rowNeighbors) + len(columnNeighbors)
    # print("first degree: ", degree)
    for rowNeighbor in rowNeighbors:
        if nodes[rowNeighbor[0] + (rowNeighbor[1] * _tableSize)].hasValue:
            degree -= 1
        else:
            continue
    for columnNeighbor in columnNeighbors:
        if nodes[columnNeighbor[0] + (columnNeighbor[1] * _tableSize)].hasValue:
            degree -= 1
        else:
            continue
    return degree


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
    x = y = 0
    for row in numericSudoku:
        for column in row:
            if column == '-':
                domain = [x + 1 for x in range(_tableSize)]
            else:
                domain = [column]
            nodes.append(Node((x, y), domain))
            # print("(x , y): ", x, " ", y)
            # print("domain: ", domain)
            # print("has value: ", nodes[x + y * _tableSize].hasValue)
            x += 1
        x = 0
        y += 1
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
    # isNeighbor = nodes[15].isNeighbor((3,0))
    # print(isNeighbor)
    # for i in range(16):
    #     print(i, " : ")
    #     x, y = nodes[i].neighbors()
    #     print(x)
    #     print(y)
    for y in range(_tableSize):
        for x in range(_tableSize):
            num = y*_tableSize + x
            # print("num: ", num)
            # print("(x , y) : ", x, y)
            # print(y*_tableSize + x, " : ")
            # x, y = nodes[y*_tableSize + x].neighbors()
            # print(x)
            # print(y)
            print(degreeCalculator(nodes[num], nodes), end=" ")
        print()



main()
