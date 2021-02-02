import re


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

    def isNeighbor(self, neighborCoordinateToCheck):
        rowNeighbors, columnNeighbors = self.neighbors()
        for row in rowNeighbors:
            if row == neighborCoordinateToCheck:
                # print("row: ", row)
                # print("finded neighbor: ", neighborCoordinateToCheck)
                return True
            else:
                continue
        for column in columnNeighbors:
            if column == neighborCoordinateToCheck:
                # print("column: ", column)
                # print("finded neighbor: ", neighborCoordinateToCheck)
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


def bestNext(nodes):
    dict = {}
    for i in range(len(nodes)):
        dict[nodes[i].position] = nodes[i].MRVSizeGetter()
    valueList = list(dict.values())
    coordianates = list(dict.keys())
    minimum = min(valueList)
    # print("minimum value", minimum)
    indices = [i for i, x in enumerate(valueList) if x == minimum]
    # print("repetation positions: ", indices)
    indexesToRemove = []
    for i in indices:
        if nodes[i].hasValue:
            indexesToRemove.append(i)
    # print("indexes to remove: ", indexesToRemove)
    for i in indexesToRemove:
        indices.remove(i)
    # print("indices to check: ", indices)
    # for i in indices:
    #     print(coordianates[i] , i)
    if len(indices) == 1:
        print("next best node finded just by MRV heuristic: ", coordianates[indices[0]])
        return coordianates[indices[0]]
    else:
        print("degree heuristic needed")
        degreeDict = {}
        for i in indices:
            degreeDict[coordianates[i]] = nodes[i].degree(nodes)
        print(degreeDict)
        remindingDegreeValueList = list(degreeDict.values())
        print(remindingDegreeValueList)
        maximumValueOfDegree = max(remindingDegreeValueList)
        print(maximumValueOfDegree)
        properNodesDict = {}
        for coordinate, degreeValue in degreeDict.items():
            if degreeValue == maximumValueOfDegree:
                properNodesDict[coordinate] = degreeValue
        print(properNodesDict)
        # print("first best node coordinates: ", list(properNodesDict.keys())[0])
        if len(properNodesDict) == 1:
            print("one sized fuck")
            return list(properNodesDict.keys())[0]
        else:
            print("more than one sized fuck")
            return list(properNodesDict.keys())[0]

def assignValue(nodes, coordinate):
    nodeNumber = coordinate[0] + coordinate[1] * _tableSize
    print(nodes[nodeNumber].position)
    print(nodes[nodeNumber].hasValue)
    print(nodes[nodeNumber].numericDomain)
    if len(nodes[nodeNumber].numericDomain) == 1:
        print("there is only one choice for assigning value to this node")
        nodes[nodeNumber].hasValue = True
    else:
        print("there is multiple choices for assigning value to this node")


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
    print("degrees : ")
    for y in range(_tableSize):
        for x in range(_tableSize):
            num = y * _tableSize + x
            print(nodes[num].degree(nodes), end=" ")
        print()

    print("MRV: ")
    for y in range(_tableSize):
        for x in range(_tableSize):
            num = y * _tableSize + x
            # print("(X,Y)", nodes[num].position)
            # print("domain: ", nodes[num].numericDomain)
            nodes[num].MRVUpdate(nodes)
            # print("list: ", nodes[num].MRVListGetter())
            # print("size: ", nodes[num].MRVSizeGetter())
    for y in range(_tableSize):
        for x in range(_tableSize):
            num = y * _tableSize + x
            print(nodes[num].MRVSizeGetter(), end=" ")
        print()

    nodeCoordinate = bestNext(nodes)
    print("best next node: ", nodeCoordinate)
    assignValue(nodes, nodeCoordinate)

main()
