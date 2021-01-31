

def extractInputFile(fileName):
    with open(fileName) as f:
        line = f.readline()
        numbers = [int(s) for s in line.split() if s.isdigit()]
        tableSize = numbers[1]
        colors = f.readline().split()
        sudukuTable = [[0 for i in range(tableSize)] for j in range(tableSize)]
        for i in range(tableSize):
            sudukuTable[i] = f.readline().split()

    return numbers, colors, sudukuTable


def main():

    numbers, colors, sudukoTable = extractInputFile("2DArray.txt")
    clolorSize, TableSize = numbers
    print(clolorSize, TableSize)
    print(colors)
    for row in sudukoTable:
        for column in row:
            print(column, end=" ")
        print()

main()