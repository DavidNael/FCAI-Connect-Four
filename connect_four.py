import numpy as np


# Constant Values
RowCount = 6
ColumnCount = 7
Blue = (0, 0, 200)
Black = (0, 0, 0)


def createBoard():
    board = np.zeros((RowCount, ColumnCount))
    return board


def putPiece(board, row, column, piece):
    board[row][column] = piece


def getRowPosition(board, column):
    for i in range(RowCount - 1, -1, -1):
        if board[i][column] == 0:
            return i


def isValidLocation(board, column):
    return board[0][column] == 0


def isWiningMove(board, mainRow, mainColumn, piece):
    # Horizontal Check

    i = mainColumn + 1
    j = mainColumn - 1
    counter = 1
    continueI = continueJ = True

    while continueI or continueJ:
        if 0 <= i <= ColumnCount - 1 and continueI:
            if board[mainRow][i] == piece:
                counter += 1
                i += 1
            else:
                continueI = False
        else:
            continueI = False
        if 0 <= j <= ColumnCount - 1 and continueJ:
            if board[mainRow][j] == piece:
                counter += 1
                j -= 1
            else:
                continueJ = False
        else:
            continueJ = False
        if counter >= 4:
            return True

    # Vertical Check

    i = mainRow + 1
    j = mainRow - 1
    counter = 1
    continueI = continueJ = True

    while continueI or continueJ:
        if 0 <= i <= RowCount - 1 and continueI:
            if board[i][mainColumn] == piece:
                counter += 1
                i += 1
            else:
                continueI = False
        else:
            continueI = False
        if 0 <= j <= RowCount - 1 and continueJ:
            if board[j][mainColumn] == piece:
                counter += 1
                j -= 1
            else:
                continueJ = False
        else:
            continueJ = False
        if counter >= 4:
            return True

    # / Cross Check
    i1 = mainRow + 1
    j1 = mainColumn - 1
    i2 = mainRow - 1
    j2 = mainColumn + 1

    counter = 1
    continueI = continueJ = True
    while continueI or continueJ:
        if 0 <= i1 <= RowCount - 1 and 0 <= j1 <= ColumnCount - 1 and continueI:
            if board[i1][j1] == piece:
                counter += 1
                i1 += 1
                j1 -= 1
            else:
                continueI = False
        else:
            continueI = False
        if 0 <= i2 <= RowCount - 1 and 0 <= j2 <= ColumnCount - 1 and continueJ:
            if board[i2][j2] == piece:
                counter += 1
                i2 -= 1
                j2 += 1
            else:
                continueJ = False
        else:
            continueJ = False
        if counter >= 4:
            return True

    # \ Cross Check
    i1 = mainRow + 1
    j1 = mainColumn + 1
    i2 = mainRow - 1
    j2 = mainColumn - 1

    counter = 1
    continueI = continueJ = True
    while continueI or continueJ:
        if 0 <= i1 <= RowCount - 1 and 0 <= j1 <= ColumnCount - 1 and continueI:
            if board[i1][j1] == piece:
                counter += 1
                i1 += 1
                j1 += 1
            else:
                continueI = False
        else:
            continueI = False
        if 0 <= i2 <= RowCount - 1 and 0 <= j2 <= ColumnCount - 1 and continueJ:
            if board[i2][j2] == piece:
                counter += 1
                i2 -= 1
                j2 -= 1
            else:
                continueJ = False
        else:
            continueJ = False
        if counter >= 4:
            return True


board = createBoard()
gameOver = False
turn = 0


while not gameOver:
    # Ask for Player 1 Input
    if turn % 2 == 0:
        selectedColumn = int(input("Player 1 Make Your Selection (1-7):")) - 1
        if isValidLocation(board, selectedColumn):
            row = getRowPosition(board, selectedColumn)
            putPiece(board, row, selectedColumn, 1)
            if isWiningMove(board, row, selectedColumn, 1):
                print(board)
                print("Player 1 Wins!!")
                break
        else:
            print("This Is Not A Valid Move")
            continue
    # Ask for Player 2 Input
    if turn % 2 != 0:
        selectedColumn = int(input("Player 2 Make Your Selection (1-7):")) - 1
        if isValidLocation(board, selectedColumn):
            row = getRowPosition(board, selectedColumn)
            putPiece(board, row, selectedColumn, 2)
            if isWiningMove(board, row, selectedColumn, 2):
                print("Player 2 Wins!!")
                break
        else:
            print("This Is Not A Valid Move")
            continue
    turn += 1
    print(board)
print("End Of Program.")
