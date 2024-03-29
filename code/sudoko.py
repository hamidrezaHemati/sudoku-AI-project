import re
from tkinter import *


class Step:
    totalStepNumber = 0

    def __init__(self, coordinate, assignedValue, stepCounter):
        self.coordinate = coordinate
        self.assignedValue = assignedValue
        self.stepCounter = stepCounter
        Step.totalStepNumber += 1

    def coordinateGetter(self):
        return self.coordinate

    def assignedValueGetter(self):
        return self.assignedValue

    def stepCounterGetter(self):
        return self.stepCounter


class Node:
    def __init__(self, position, numericDomain, colorDomain):
        self.position = position
        self.numericDomain = numericDomain
        self.colorDomain = colorDomain
        if len(numericDomain) == 1:
            self.hasValue = True
            self.assignedValue = numericDomain[0]
        else:
            self.hasValue = False
        if len(colorDomain) == 1:
            self.hasColor = True
            self.assignedColor = colorDomain[0]
        else:
            self.hasColor = False

    def display(self):
        print("informations: ")
        print("X Y ", self.position)
        print("value: ", self.numericDomain)
        print("value: ", self.colorDomain)
        print("has value: ", self.hasValue)
        print("has value: ", self.hasColor)

    def assignedValueGetter(self):
        return self.assignedValue

    def neighbors(self):
        rowNeighbors = []
        columnNeighbors = []
        for i in range(_tableSize):
            if i != self.position[0]:
                neighbor = (i, self.position[1])
                rowNeighbors.append(neighbor)
            if i != self.position[1]:
                neighbor = (self.position[0], i)
                columnNeighbors.append(neighbor)
        return rowNeighbors, columnNeighbors

    def adjacentNeighbor(self):
        rowNeighbors, columnNeighbors = self.neighbors()

        adjacentRow = []
        adjacentCol = []
        for row in rowNeighbors:
            if abs(row[0] - self.position[0]) == 1:
                adjacentRow.append(row)
        for col in columnNeighbors:
            if abs(col[1] - self.position[1]) == 1:
                adjacentCol.append(col)
        return adjacentRow, adjacentCol

    def isNeighbor(self, neighborCoordinateToCheck):
        rowNeighbors, columnNeighbors = self.neighbors()
        for row in rowNeighbors:
            if row == neighborCoordinateToCheck:
                return True
            else:
                continue
        for column in columnNeighbors:
            if column == neighborCoordinateToCheck:
                return True
            else:
                continue
        return False

    def degree(self, nodes):
        rowNeighbors, columnNeighbors = self.neighbors()
        degree = len(rowNeighbors) + len(columnNeighbors)
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

    def MRVUpdate(self, nodes):
        rowNeighbors, columnNeighbors = self.neighbors()
        reservedValues = []
        for row in rowNeighbors:
            if nodes[row[0] + row[1] * _tableSize].hasValue:
                reservedValues.append(nodes[row[0] + row[1] * _tableSize].numericDomain)
        for column in columnNeighbors:
            if nodes[column[0] + column[1] * _tableSize].hasValue:
                if nodes[column[0] + column[1] * _tableSize].numericDomain not in reservedValues:
                    reservedValues.append(nodes[column[0] + column[1] * _tableSize].numericDomain)
        for i in range(len(reservedValues)):
            reservedValues[i] = reservedValues[i][0]
        updatedDomain = []
        for value in self.numericDomain:
            if value not in reservedValues:
                updatedDomain.append(value)
        # print("neighbors reserved: ", reservedValues)
        # print("new Domain: ", updatedDomain)
        self.numericDomain = updatedDomain

    def MRVSizeGetter(self):
        return len(self.numericDomain)

    def MRVListGetter(self):
        return self.numericDomain


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


def NodeMaker(numericSudoku, sudokuTable, colors):
    nodes = []
    x = y = 0
    print("check dimensions sudoku table: ")
    for y in range(_tableSize):
        for x in range(_tableSize):
            print(sudokuTable[y][x])
        print()

    print()
    print("check dimensions numeric sudoku table: ")
    for y in range(_tableSize):
        for x in range(_tableSize):
            print(numericSudoku[y][x])
        print()
    print()
    for y in range(_tableSize):
        for x in range(_tableSize):
            if numericSudoku[y][x] == '-':
                domain = [x + 1 for x in range(_tableSize)]
            else:
                domain = []
                domain.append(numericSudoku[y][x])
            colorDomain = re.findall("[a-z]", sudokuTable[y][x])
            if len(colorDomain) == 0:
                colorDomain = [color for color in colors]

            nodes.append(Node((x, y), domain, colorDomain))
            # print("(x , y): ", x, " ", y)
            # print("domain: ", domain)
            # print("has value: ", nodes[x + y * _tableSize].hasValue)
            x += 1
        x = 0
        y += 1
    return nodes


def minimumRemainingValues(nodes):
    dict = {}
    for i in range(len(nodes)):
        dict[nodes[i].position] = nodes[i].MRVSizeGetter()
    valueList = list(dict.values())
    coordianates = list(dict.keys())
    valueListForNotAssignedNodes = []
    for i in coordianates:
        if not nodes[i[0] + i[1] * _tableSize].hasValue:
            valueListForNotAssignedNodes.append(dict[i])
    minimum = min(valueListForNotAssignedNodes)
    indices = [i for i, x in enumerate(valueList) if x == minimum]
    indexesToRemove = []
    for i in indices:
        if nodes[i].hasValue:
            indexesToRemove.append(i)
    for i in indexesToRemove:
        indices.remove(i)
    return coordianates, indices


def bestNextNode(nodes):
    coordianates, indices = minimumRemainingValues(nodes)
    # print("coordinates fuuuck: ", coordianates)
    # print("indecis fuuuck: ", indices)
    # print("MRV candidates reminding after finding MRV: ", end=" ")
    # for i in indices:
    #     print(coordianates[i], end=" ")
    # print()
    if len(indices) == 1:
        return coordianates[indices[0]]
    else:
        degreeDict = {}
        for i in indices:
            degreeDict[coordianates[i]] = nodes[i].degree(nodes)
        remindingDegreeValueList = list(degreeDict.values())
        maximumValueOfDegree = max(remindingDegreeValueList)
        properNodesDict = {}
        for coordinate, degreeValue in degreeDict.items():
            if degreeValue == maximumValueOfDegree:
                properNodesDict[coordinate] = degreeValue
        if len(properNodesDict) == 1:
            return list(properNodesDict.keys())[0]
        else:
            return list(properNodesDict.keys())[0]


def draw(nodes):
    for row in range(_tableSize):
        for col in range(_tableSize):
            if nodes[col + row * _tableSize].hasValue:
                print(nodes[col + row * _tableSize].assignedValue, end=" ")
            else:
                print("-", end=" ")
        print()


def displaySudokuTable(_table):
    for row in _table:
        for column in row:
            print(column, end=" ")
        print()


def updateMRV(nodes):
    for y in range(_tableSize):
        for x in range(_tableSize):
            num = y * _tableSize + x
            # print("(X,Y)", nodes[num].position)
            # print("domain: ", nodes[num].numericDomain)
            nodes[num].MRVUpdate(nodes)
            # print("list: ", nodes[num].MRVListGetter())
            # print("size: ", nodes[num].MRVSizeGetter())


global stepNumber
stepNumber = 0


# return false if there is node without any assignment options
# return true if everything is fine
def forwardChecking(nodes):
    updateMRV(nodes)
    # print("MRV: ")
    # for y in range(_tableSize):
    #     for x in range(_tableSize):
    #         num = y * _tableSize + x
    #         print(nodes[num].MRVSizeGetter(), end=" ")
    #     print()
    for node in nodes:
        if node.MRVSizeGetter() == 0:
            return False
    return True


# return False if the problem dos not hav solution
# return true if backtrack is finished successfully
def backTrack(nodes, path):
    i = 1
    while not forwardChecking(nodes):
        print("back track number: ", i)
        if len(path) == 0:
            return False
        removed = path.pop()
        removedNodeNumber = removed.coordinate[0] + removed.coordinate[1] * _tableSize
        nodes[removedNodeNumber].hasValue = False
        nodes[removedNodeNumber].numericDomain.remove(removed.assignedValue)
        rowNeighbors, columnNeighbors = nodes[removedNodeNumber].neighbors()
        for node in rowNeighbors:
            nodes[node[0] + node[1] * _tableSize].numericDomain.append(removed.assignedValue)
        for node in columnNeighbors:
            nodes[node[0] + node[1] * _tableSize].numericDomain.append(removed.assignedValue)
        updateMRV(nodes)
        # print("MRV: ")
        # for y in range(_tableSize):
        #     for x in range(_tableSize):
        #         num = y * _tableSize + x
        #         print(nodes[num].MRVSizeGetter(), end=" ")
        #     print()
        i += 1
        for y in range(_tableSize):
            for x in range(_tableSize):
                num = y * _tableSize + x
                print(nodes[num].numericDomain, end=" ")
            print()
    return True


# returns true when table is solved
def endGameCheck(nodes):
    for node in nodes:
        if not node.hasValue:
            return False
    return True


def solve(nodes, path):
    global stepNumber
    while True:
        if endGameCheck(nodes):
            break
        nextNode = bestNextNode(nodes)
        nodeNumber = nextNode[0] + nextNode[1] * _tableSize
        # print("NUMBER OF VALUES IN NODE DOMAIN: ", len(nodes[nodeNumber].numericDomain))
        nodes[nodeNumber].assignedValue = nodes[nodeNumber].numericDomain[0]
        nodes[nodeNumber].hasValue = True
        step = Step(nextNode, nodes[nodeNumber].assignedValue, stepNumber)
        path.append(step)
        stepNumber += 1
        # draw(nodes)

        if forwardChecking(nodes):
            continue
        else:
            print("BACK TRACKING")
            if not backTrack(nodes, path):
                return False
    return True


def main():
    global _tableSize
    global colorSize
    numbers, colors, sudokuTable = extractInputFile("test.txt")
    colorSize, _tableSize = numbers
    print(colorSize, _tableSize)
    print(colors)
    displaySudokuTable(sudokuTable)
    numericSudoku = numericSudokuMaker(sudokuTable)
    nodes = NodeMaker(numericSudoku, sudokuTable, colors)
    for node in nodes:
        node.display()
    draw(nodes)
    for y in range(_tableSize):
        for x in range(_tableSize):
            num = y * _tableSize + x
            nodes[num].MRVUpdate(nodes)
    print("--------------------------------------------")
    path = []
    if not solve(nodes, path):
        print("this table dos'nt have an answer")
    else:
        print()
        print("solved sudoku table: ")
        draw(nodes)
    for i in path:
        print("#########")
        print("step number: ", i.stepCounter)
        print("selected coordinate: ", i.coordinate)
        print("assigned value: ", i.assignedValue)


main()
