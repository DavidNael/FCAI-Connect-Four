import random
import numpy as np
import pygame
import sys
import math
import time

# Initialize Pygame
pygame.init()


# Constant Values
EmptyPiece = 0
PlayerOnePiece = 1
PlayerTwoPiece = 2
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
GameFont = pygame.font.SysFont("monospace", 75)


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
    return bool(board[0][column] == EmptyPiece)


def getAllValidLocations(board):
    locations = []
    for column in range(ColumnCount):
        if isValidLocation(board, column):
            locations.append(column)
    return locations


def isDraw(board):
    for i in range(ColumnCount):
        if board[0][i] == EmptyPiece:
            return False
    return True


def isEmptyBoard(board):
    for i in range(ColumnCount):
        if board[RowCount - 1][i] != EmptyPiece:
            return False
    return True


def isWiningMove(board, mainRow, mainColumn, piece):
    directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]  # list of all possible directions
    for directionX, directionY in directions:
        counter = 1
        x, y = mainColumn + directionX, mainRow + directionY
        while 0 <= x < ColumnCount and 0 <= y < RowCount and board[y][x] == piece:
            counter += 1
            x, y = x + directionX, y + directionY
        x, y = mainColumn - directionX, mainRow - directionY
        while 0 <= x < ColumnCount and 0 <= y < RowCount and board[y][x] == piece:
            counter += 1
            x, y = x - directionX, y - directionY
        if counter >= 4:
            return True
    return False


def evaluateWindowScore(window, piece):
    score = 0
    opponentPiece = PlayerOnePiece if piece == PlayerTwoPiece else PlayerTwoPiece

    # 1 Scoring Points For Positive Move
    if window.count(piece) == 4:
        return (100000, True)
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    # 1 Scoring Points For Negative Moves
    if window.count(opponentPiece) == 3 and window.count(0) == 1:
        score -= 8
    return (score, False)


def getMoveScore(board, piece):
    score = 0
    # 1 Horizontal Score
    for row in range(RowCount):
        rowArray = [int(i) for i in list(board[row, :])]  # Get Row Of i as List
        for column in range(ColumnCount - 3):
            window = rowArray[column : column + 4]
            newScore, isWin = evaluateWindowScore(window, piece)
            if isWin:
                return 1000000000
            score += newScore
    # 2 Vertical Score
    for column in range(ColumnCount):
        columnArray = [int(i) for i in list(board[:, column])]  # Get Row Of i as List
        for row in range(RowCount - 3):
            window = columnArray[row : row + 4]
            newScore, isWin = evaluateWindowScore(window, piece)
            if isWin:
                return 1000000000
            score += newScore
    # 3 / Diagonal Score
    for row in range(RowCount - 3):
        for column in range(ColumnCount - 3):
            window = [board[row + counter][column + counter] for counter in range(4)]
            newScore, isWin = evaluateWindowScore(window, piece)
            if isWin:
                return 1000000000
            score += newScore
    # 4 \ Diagonal Score
    for row in range(RowCount - 3):
        for column in range(ColumnCount - 3):
            window = [
                board[row + 3 - counter][column + counter] for counter in range(4)
            ]
            newScore, isWin = evaluateWindowScore(window, piece)
            if isWin:
                return 1000000000
            score += newScore
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


# 1 MiniMax Algorithm
def minimax(board, depth, alpha, beta, maximizePlayer, player):
    validLocations = getAllValidLocations(board)
    bestColumn = random.choice(validLocations)
    oppositePlayer = PlayerOnePiece if player == PlayerTwoPiece else PlayerTwoPiece
    if depth == 0:
        return (getMoveScore(board, player), bestColumn)
    if isEmptyBoard(board):
        return (10000, int(math.floor(ColumnCount / 2)))
    if maximizePlayer:
        score = -math.inf
        for column in validLocations:
            row = getRowPosition(board, column)
            simulationBoard = board.copy()
            if putPiece(simulationBoard, row, column, player):
                return (10000, column)
            newScore = minimax(
                simulationBoard, depth - 1, alpha, beta, not maximizePlayer, player
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
            if putPiece(simulationBoard, row, column, oppositePlayer):
                return (-10000, column)
            newScore = minimax(
                simulationBoard, depth - 1, alpha, beta, not maximizePlayer, player
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
            if board[row][column] == EmptyPiece:
                circleColor = Black
            elif board[row][column] == PlayerOnePiece:
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


def renderMainMenu(screen):
    # 1 Set up the font and text
    font = pygame.font.SysFont(None, 50)

    titleText = font.render("Connect 4", True, (255, 255, 255))
    titleRect = titleText.get_rect(center=(350, 100))

    twoPlayerText = font.render("Player VS Player", True, (255, 255, 255))
    twoPlayerRect = twoPlayerText.get_rect(center=(350, 300))

    oneAiOnePlayerText = font.render("Player VS AI", True, (255, 255, 255))
    oneAiOnePlayerTextRect = oneAiOnePlayerText.get_rect(center=(350, 400))

    twoAIText = font.render("AI VS AI", True, (255, 255, 255))
    twoAIRect = twoAIText.get_rect(center=(350, 500))

    # 1 Draw the menu on the screen
    screen.fill((0, 0, 0))
    screen.blit(titleText, titleRect)
    screen.blit(twoPlayerText, twoPlayerRect)
    screen.blit(oneAiOnePlayerText, oneAiOnePlayerTextRect)
    screen.blit(twoAIText, twoAIRect)

    # 1 Update the display
    pygame.display.update()

    # 1 Wait for the player to choose an option
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if twoPlayerRect.collidepoint(pos):
                    return 0
                elif oneAiOnePlayerTextRect.collidepoint(pos):
                    return 1
                elif twoAIRect.collidepoint(pos):
                    return 2


def clearBoard():
    pygame.draw.rect(screen, Black, (0, 0, width, SquareSize))


def renderPlayerCircle(xPosition, color):
    clearBoard()
    pygame.draw.circle(screen, color, (xPosition, int(SquareSize / 2)), radius)
    pygame.display.update()


def playTurn(board, selectedColumn, pieceColor, playerNumber):
    # 1 If The Selected Column Is Not Full Of Pieces
    if isValidLocation(board, selectedColumn):
        nextAvailableRow = getRowPosition(board, selectedColumn)

        # 2 If Player Placed Wining Piece
        if putPiece(board, nextAvailableRow, selectedColumn, playerNumber):
            clearBoard()
            label = GameFont.render(
                "Player " + str(playerNumber) + " Wins !!", 1, pieceColor
            )
            screen.blit(label, (20, 10))
            print("Player " + str(playerNumber) + " Wins !!")
            return True

        # 2 If The Board Is Completely Full
        if isDraw(board):
            clearBoard()
            label = GameFont.render("Draw !!", 1, Gray)
            screen.blit(label, (180, 10))
            print("Draw !!")
            return True
    # 1 If The Selected Column Is Full
    else:
        print("This Is Not A Valid Move")
    return False


# 1 Initialize the Game Window
screen = pygame.display.set_mode(size)

# 1 Initialize Game Option
gameOption = renderMainMenu(screen)
board = createBoard()
isGameOver = False
turn = random.randint(0, 1)

clearBoard()
renderBoard(board)

while not isGameOver:
    for event in pygame.event.get():
        # 1 Get Current Turn
        if turn % 2 == 0:
            pieceColor = Red
            playerNumber = PlayerOnePiece
        else:
            pieceColor = Yellow
            playerNumber = PlayerTwoPiece

        # 1 If Player Exit The Game
        if event.type == pygame.QUIT:
            sys.exit()

        # 1 If Player Move The Mouse
        if event.type == pygame.MOUSEMOTION and gameOption != 2:
            xPosition = event.pos[0]
            renderPlayerCircle(xPosition, pieceColor)

        # 1 If It Is Human Player
        if event.type == pygame.MOUSEBUTTONDOWN and (
            gameOption == 0 or gameOption == 1
        ):
            xPosition = event.pos[0]
            selectedColumn = int(math.floor(xPosition / SquareSize))

            # 2 If Player Is Player 1
            if turn % 2 == 0:
                pieceColor = Red
                playerNumber = PlayerOnePiece

            # 2 If Player Is Player 2
            else:
                pieceColor = Yellow
                playerNumber = PlayerTwoPiece

            # 2 Render Second Piece When First piece Is Dropped
            if gameOption == 0:
                renderPlayerCircle(xPosition, Red if pieceColor == Yellow else Yellow)

            # 2 Put The Piece
            isGameOver = playTurn(board, selectedColumn, pieceColor, playerNumber)

            turn += 1
            print(board)
            renderBoard(board)

    # 1 If It Is AI Turn
    if not isGameOver and (gameOption == 1 or gameOption == 2):
        if turn % 2 == 0 and gameOption == 2:
            pieceColor = Red
            playerNumber = PlayerOnePiece
        elif turn % 2 != 0:
            pieceColor = Yellow
            playerNumber = PlayerTwoPiece
            # selectedColumn = pickBestMove(board, playerNumber)
        else:
            continue
        startTime = time.time()
        selectedColumn = minimax(board, 6, -math.inf, math.inf, True, playerNumber)[1]
        endTime = time.time()
        if endTime - startTime < 0.5:
            pygame.time.wait(500)
        print("Selected AI Column = ", selectedColumn)
        while not isValidLocation(board, selectedColumn):
            selectedColumn = random.randint(0, ColumnCount - 1)

        isGameOver = playTurn(board, selectedColumn, pieceColor, playerNumber)
        turn += 1
        print(board)
        renderBoard(board)
    if isGameOver:
        pygame.time.wait(5000)
print("End Of Program.")
