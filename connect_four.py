import random
import numpy as np
import pygame
import sys
import math

# Initialize Pygame
pygame.init()


# Constant Values
RowCount = 6
ColumnCount = 7
SquareSize = 100
Blue = (0, 0, 200)
Black = (0, 0, 0)
Yellow = (228, 205, 5)
Red = (200, 20, 20)
Gray = (211, 211, 211)

# GUI Dimensions
width = ColumnCount * SquareSize
height = (RowCount + 1) * SquareSize

size = (width, height)
radius = int(SquareSize / 2 - 5)

# Fonts
WiningFont = pygame.font.SysFont("monospace", 75)


def createBoard():
    board = np.zeros((RowCount, ColumnCount))
    return board


def putPiece(board, row, column, piece):
    board[row][column] = piece
    if isWiningMove(board, row, column, piece):
        return True
    else:
        return False


def getRowPosition(board, column):
    for i in range(RowCount - 1, -1, -1):
        if board[i][column] == 0:
            return i


def isValidLocation(board, column):
    return board[0][column] == 0


def getAllValidLocations(board):
    locations = []
    for column in range(ColumnCount):
        if isValidLocation(board, column):
            locations.append(column)
    return locations


def isDraw(board):
    for i in range(ColumnCount):
        if board[0][i] == 0:
            return False
    return True


def isWiningMove(board, mainRow, mainColumn, piece):
    # 1 Horizontal Check

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

    # 2 Vertical Check

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

    # 3 / Cross Check
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

    # 4 \ Cross Check
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


def evaluateWindowScore(window, piece):
    score = 0
    opponentPiece = 1 if piece == 2 else 2

    # 1 Scoring Points For Positive Move
    if window.count(piece) == 4:
        score += 100000
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    # 1 Scoring Points For Negative Moves
    if window.count(opponentPiece) == 3 and window.count(0) == 1:
        score -= 8
    return score


def getMoveScore(board, piece):
    score = 0
    # 1 Horizontal Score
    for row in range(RowCount):
        rowArray = [int(i) for i in list(board[row, :])]  # Get Row Of i as List
        for column in range(ColumnCount - 3):
            window = rowArray[column : column + 4]
            score += evaluateWindowScore(window, piece)
    # 2 Vertical Score
    for column in range(ColumnCount):
        columnArray = [int(i) for i in list(board[:, column])]  # Get Row Of i as List
        for row in range(RowCount - 3):
            window = columnArray[row : row + 4]
            score += evaluateWindowScore(window, piece)
    # 3 / Diagonal Score
    for row in range(RowCount - 3):
        for column in range(ColumnCount - 3):
            window = [board[row + counter][column + counter] for counter in range(4)]
            score += evaluateWindowScore(window, piece)
    # 4 \ Diagonal Score
    for row in range(RowCount - 3):
        for column in range(ColumnCount - 3):
            window = [
                board[row + 3 - counter][column + counter] for counter in range(4)
            ]
            score += evaluateWindowScore(window, piece)
    # 5 Center Score
    centerArray = [int(i) for i in list(board[:, ColumnCount // 2])]
    score += centerArray.count(piece) * 3
    return score


def pickBestMove(board, piece):
    validLocations = getAllValidLocations(board)
    bestScore = -1000
    bestMove = random.choice(validLocations)
    for column in validLocations:
        simulationBoard = board.copy()
        row = getRowPosition(simulationBoard, column)
        putPiece(simulationBoard, row, column, piece)
        currentScore = getMoveScore(simulationBoard, piece)
        if currentScore > bestScore:
            bestScore = currentScore
            bestMove = column
    return bestMove


def isTerminalNode(board):
    # 1 Horizontal Check
    for row in range(RowCount):
        rowArray = [int(i) for i in list(board[row, :])]  # Get Row Of i as List
        for column in range(ColumnCount - 3):
            window = rowArray[column : column + 4]
            if window.count(1) == 4:
                return 1
            elif window.count(2) == 4:
                return 2
    # 2 Vertical Check
    for column in range(ColumnCount):
        columnArray = [int(i) for i in list(board[:, column])]  # Get Row Of i as List
        for row in range(RowCount - 3):
            window = columnArray[row : row + 4]
            if window.count(1) == 4:
                return 1
            elif window.count(2) == 4:
                return 2
    # 3 / Diagonal Check
    for row in range(RowCount - 3):
        for column in range(ColumnCount - 3):
            window = [board[row + counter][column + counter] for counter in range(4)]
            if window.count(1) == 4:
                return 1
            elif window.count(2) == 4:
                return 2
    # 4 \ Diagonal Check
    for row in range(RowCount - 3):
        for column in range(ColumnCount - 3):
            window = [
                board[row + 3 - counter][column + counter] for counter in range(4)
            ]
            if window.count(1) == 4:
                return 1
            elif window.count(2) == 4:
                return 2
    # 5 Draw Check
    if isDraw(board):
        return 3
    return 0


# 1 MiniMax Algorithm
def minimax(board, depth, alpha, beta, maximizePlayer):
    currentState = isTerminalNode(board)
    if depth == 0 or currentState != 0:
        if currentState != 0:
            if currentState == 1:
                return (-10000, None)
            elif currentState == 2:
                return (10000, None)
            else:
                return (0, None)
        else:
            return (getMoveScore(board, 2), None)
    validLocations = getAllValidLocations(board)
    bestColumn = random.choice(validLocations)
    if maximizePlayer:
        score = -math.inf
        for column in validLocations:
            row = getRowPosition(board, column)
            simulationBoard = board.copy()
            if putPiece(simulationBoard, row, column, 2):
                return (10000, column)
            newScore = minimax(
                simulationBoard, depth - 1, alpha, beta, not maximizePlayer
            )[0]

            if newScore > score:
                score = newScore
                bestColumn = column
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        return (score, bestColumn)
    else:
        score = math.inf
        for column in validLocations:
            row = getRowPosition(board, column)
            simulationBoard = board.copy()
            if putPiece(simulationBoard, row, column, 1):
                return (-10000, column)
            newScore = minimax(
                simulationBoard, depth - 1, alpha, beta, not maximizePlayer
            )[0]
            if newScore < score:
                score = newScore
                bestColumn = column
            beta = min(beta, score)
            if alpha >= beta:
                break
        return (score, bestColumn)


# GUI Functions
def renderBoard(board):
    for row in range(RowCount):
        for column in range(ColumnCount):
            pygame.draw.rect(
                screen,
                Blue,
                (
                    column * SquareSize,  # X-Position
                    row * SquareSize + SquareSize,  # Y-Position
                    SquareSize,  # Width
                    SquareSize,  # height
                ),
            ),
            if board[row][column] == 0:
                circleColor = Black
            elif board[row][column] == 1:
                circleColor = Red
            else:
                circleColor = Yellow

            circleCenterX = column * SquareSize + SquareSize / 2
            circleCenterY = row * SquareSize + SquareSize + SquareSize / 2

            pygame.draw.circle(
                screen,
                circleColor,
                (
                    circleCenterX,
                    circleCenterY,
                ),
                radius,
            )
            pygame.display.update()


def clearBoard():
    pygame.draw.rect(screen, Black, (0, 0, width, SquareSize))


def renderPlayerCircle(xPosition, color):
    clearBoard()
    pygame.draw.circle(screen, color, (xPosition, int(SquareSize / 2)), radius)
    pygame.display.update()


board = createBoard()
gameOver = False
turn = random.randint(0, 1)

screen = pygame.display.set_mode(size)
renderBoard(board)


while not gameOver:
    for event in pygame.event.get():
        # 1 Get Current Turn
        if turn % 2 == 0:
            pieceColor = Red
            playerNumber = 1
        else:
            pieceColor = Yellow
            playerNumber = 2

        # 1 If Player Exit The Game
        if event.type == pygame.QUIT:
            sys.exit()

        # 1 If Player Move The Mouse
        if event.type == pygame.MOUSEMOTION:
            xPosition = event.pos[0]
            renderPlayerCircle(xPosition, pieceColor)

        # 1 If Player Press The Mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            xPosition = event.pos[0]
            selectedColumn = int(math.floor(xPosition / SquareSize))
            # 2 If Player Is Player 1 (Human)
            if turn % 2 == 0:
                pieceColor = Red
                playerNumber = 1
                # renderPlayerCircle(xPosition, Red if pieceColor == Yellow else Yellow)

                # 3 If The Selected Column Is Not Full Of Pieces
                if isValidLocation(board, selectedColumn):
                    nextAvailableRow = getRowPosition(board, selectedColumn)
                    putPiece(board, nextAvailableRow, selectedColumn, playerNumber)

                    # 4 If Player Placed Wining Piece
                    if isWiningMove(
                            board, nextAvailableRow, selectedColumn, playerNumber
                    ):
                        clearBoard()
                        label = WiningFont.render(
                            "Player " + str(playerNumber) + " Wins !!", 1, pieceColor
                        )
                        screen.blit(label, (20, 10))
                        print("Player " + str(playerNumber) + " Wins !!")
                        gameOver = True

                    # 4 If The Board Is Completely Full
                    if isDraw(board):
                        clearBoard()
                        label = WiningFont.render("Draw !!", 1, Gray)
                        screen.blit(label, (180, 10))
                        print("Draw !!")
                        gameOver = True
                # 3 If The Selected Column Is Full
                else:
                    print("This Is Not A Valid Move")
                    continue

            turn += 1
            print(board)
            renderBoard(board)

    # 1 If It Is Player 2 Turn (AI)
    if turn % 2 != 0 and not gameOver:
        pieceColor = Yellow
        playerNumber = 2
        # selectedColumn = pickBestMove(board, playerNumber)
        score, selectedColumn = minimax(board, 6, -math.inf, math.inf, True)
        while not isValidLocation(board, selectedColumn):
            selectedColumn = random.randint(0, ColumnCount - 1)
        nextAvailableRow = getRowPosition(board, selectedColumn)
        putPiece(board, nextAvailableRow, selectedColumn, playerNumber)
        if isWiningMove(board, nextAvailableRow, selectedColumn, playerNumber):
            clearBoard()
            label = WiningFont.render(
                "Player " + str(playerNumber) + " Wins !!", 1, pieceColor
            )
            screen.blit(label, (20, 10))
            print("Player " + str(playerNumber) + " Wins !!")
            gameOver = True
        turn += 1
        print(board)
        renderBoard(board)
    if gameOver:
        pygame.time.wait(3000)
print("End Of Program.")
