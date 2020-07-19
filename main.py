import chess
import chess.pgn
import math
from collections.abc import Mapping
from random import randrange

board = chess.Board()
legalMoves = []

maxMoves = 1000
maxGames = 1

def getLegalMoves(board):
    legalMoves = []

    for move in board.legal_moves:
        legalMoves.append(move)
    return legalMoves

def split(word):
    return [char for char in word]

def isDict(variable):
    return isinstance(variable, Mapping)

currentDepth = 0
movesMade = 0

def makeBoardMove(board, move):
    global currentDepth
    if move != "":
        board.push(chess.Move.from_uci(move))
        currentDepth += 1

    return board

def resetBoard(board):
    global currentDepth
    #print("resetting depth: ", currentDepth)

    while currentDepth - movesMade != 0:
        board.pop()
        currentDepth -= 1

def resetBoardX(board, steps):
    global currentDepth
    #print("resetting depth x: ", currentDepth)

    for step in range(steps):
        if currentDepth - movesMade != 0:
            currentDepth -= 1
            board.pop()

def getScorePieces(board):
    chars = split(str(board))

    score = 0

    if board.is_stalemate():
        #print("HYPOTHETICAL STALEMATE")
        return 0

    if board.can_claim_draw():
        # todo do min/max depending if below/over 0
        # print("CAN CLAIM DRAW")
        return 0

    i = 0

    for char in chars:
        if char == ' ' or char == '\n':
            continue

        row = int(i/8)
        column = i%8
        i += 1

        distanceToCenter = math.sqrt((row-3.5)**2 + (column-3.5)**2)

        positionValue = -(distanceToCenter/1000000.0)

        #print("distance", multiplier)


        # Black pieces
        if char == "r":
            score -= 5
            score -= positionValue
        elif char == "n":
            score -= 2.9
            score -= positionValue
        elif char == "q":
            score -= 9
            score -= positionValue
        elif char == "b":
            score -= 3
            score -= positionValue
        elif char == "k":
            score -= 1000
            score += positionValue
        elif char == "p":
            score -= 1
            score -= positionValue

        # White pieces
        elif char == "R":
            score += 5
            score += positionValue
        elif char == "N":
            score += 2.9
            score += positionValue
        elif char == "Q":
            score += 9
            score += positionValue
        elif char == "B":
            score += 3
            score += positionValue
        elif char == "K":
            score += 1000
            score -= positionValue
        elif char == "P":
            score += 1
            score += positionValue

    #print(board)
    #print(score)
    return score

def getMoveRandom(board):
    legalMoves = getLegalMoves(board)
    #print("legal moves: ", len(legalMoves))

    moveIndex = randrange(0, len(legalMoves))
    return str(legalMoves[moveIndex])


def getFirstMove(board):
    legalMoves = getLegalMoves(board)
    return str(legalMoves[0])

def getBestMove1Depth(board):

    legalMoves = getLegalMoves(board)

    if len(legalMoves) == 0:
        return ""

    bestScore = -10000
    colorScoreCorrection = 1
    bestMove = ""

    if board.turn == chess.BLACK:
        colorScoreCorrection = -1

    for move in legalMoves:
        move = str(move)

        #board.push(chess.Move.from_uci(move))
        makeBoardMove(board, move)

        moveScore = getScorePieces(board) * colorScoreCorrection

        if moveScore > bestScore:
            bestScore = moveScore
            bestMove = move

        resetBoardX(board, 1)

    return bestMove

def getScoreAfterMove(board, move):
    move = str(move)
    makeBoardMove(board, move)
    score = getScorePieces(board)

    resetBoardX(board, 1)

    return score

def getBestMoveSearchTree(board, nNodes):

    bestMove = getMoveRandom(board)

    scores = {}

    searchedNodes = 0

    boardToSearch = board

    queue = []

    currentDepth = 0

    legalMoves = getLegalMoves(board)

    if len(legalMoves) == 0:
        return ""

    for move in legalMoves:
        scores[move] = getScoreAfterMove(board, move)

    sortedScores = sorted(scores.items(), key=lambda x: x[1])
    scores = sortedScores

    # always start from current board state
    while(searchedNodes < nNodes):
        searchedNodes += 1

        if board.turn == chess.WHITE:
            bestMove = str(sortedScores[len(sortedScores)-1][0])

            pass
        elif board.turn == chess.BLACK:
            bestMove = str(sortedScores[0][0])

            pass


        #sortedScores = sorted(scores.items(), key=lambda x: x[1])
        #scores = sortedScores




        if False:
            for tuple in scores:
                move = tuple[0]
                score = tuple[1]

                for i in range(len(sortedScores)):
                    queue.append(move)



            boardToSearch = makeBoardMove(bestMove)



    #sortedScores = sorted(scores.items(), key=lambda x: x[1])

    if board.turn == chess.WHITE:
        # take last element "highest score"
        bestMove = str(sortedScores[len(sortedScores)-1][0])
    elif board.turn == chess.BLACK:
        # take first element "lowest score"
        bestMove = str(sortedScores[0][0])


    scores = sortedScores

    print("sorted:", sortedScores)



    if False:
        for key in scores:
            print("score", key, " : ", scores[key])

        for i in sorted (scores):
            print("move :", scores[i])
            print("moveI:", i)

    return bestMove


def getBestMove2Depth(board):

    legalMoves = getLegalMoves(board)

    bestScore = -10000
    colorScoreCorrection = 1
    bestMove = ""

    if board.turn == chess.BLACK:
        colorScoreCorrection = -1

    for move in legalMoves:
        move = str(move)

        makeBoardMove(board, move)
        bestOpponentMove = getBestMove1Depth(board)
        makeBoardMove(board, bestOpponentMove)

        scoreD2 = getScorePieces(board) * colorScoreCorrection


        if scoreD2 > bestScore:
            bestScore = scoreD2
            bestMove = move

        resetBoard(board)

    return bestMove


def getBestMove3Depth(board):

    legalMoves = getLegalMoves(board)

    bestScore = -10000
    colorScoreCorrection = 1
    bestMove = ""

    if board.turn == chess.BLACK:
        colorScoreCorrection = -1

    for move in legalMoves:
        move = str(move)

        makeBoardMove(board, move)
        bestOpponentMove = getBestMove2Depth(board)
        makeBoardMove(board, bestOpponentMove)

        scoreD2 = getScorePieces(board) * colorScoreCorrection *-1


        if scoreD2 > bestScore:
            bestScore = scoreD2
            bestMove = move

        resetBoard(board)

    return bestMove


def getBestMove2Depthv2(board):

    legalMoves = getLegalMoves(board)

    bestScore = -10000
    colorScoreCorrection = 1
    bestMove = ""

    if board.turn == chess.BLACK:
        colorScoreCorrection = -1

    for move in legalMoves:
        move = str(move)

        board.push(chess.Move.from_uci(move))



        # opponent makes a move
        bestOpponentMove = getBestMove1Depth(board)
        board.push(chess.Move.from_uci(bestOpponentMove))

        #responding move
        legalMoves = getLegalMoves(board)
        for moveDepth2 in legalMoves:
            moveDepth2 = str(moveDepth2)

            board.push(chess.Move.from_uci(moveDepth2))

            moveScoreDepth2 = getScorePieces(board)
            if moveScoreDepth2 > bestScore:
                bestScore = moveScoreDepth2
                bestMove = move

            #reset until opponent move
            board.pop()

        #reset opponent move
        board.pop()


        #moveScore = getScorePieces(board) * colorScoreCorrection


        # Reset board
        board.pop()

    return bestMove


def getBestMoveDepth2(board):

    #print("iteration@@@@@@@@@@@@@@@@@@@@@@@@@")

    legalMoves = getLegalMoves(board)

    bestScore = -10000
    colorScoreCorrection = 1
    bestMove = ""

    if board.turn == chess.BLACK:
        colorScoreCorrection = -1

    for move in legalMoves:
        move = str(move)

        #print("starting state: ")
        #print(board)

        #print("trying new move")

        #print("1_______")
        #print(board)

        #board.push(chess.Move.from_uci(move))

        makeBoardMove(board, move)

        #print("_____________________")
        #print("move: ", move)
        #print(getScorePieces(board))
        #print(board)

        #print("turn: ", board.turn)

        #print(board)

        # opponent makes a "good" move
        bestOpponentMove = getBestMove1Depth(board)
        #print("bom: ", bestOpponentMove)
        #board.push(chess.Move.from_uci(bestOpponentMove))
        makeBoardMove(board, bestOpponentMove)

        #print("------")
        #print("move: ", bestOpponentMove)
        #print(getScorePieces(board))
        #print(board)
        #print("turn: ", board.turn)




        #print("3_______")
        #print(board)


        bestMoveDepth2 = getBestMove1Depth(board)
        #board.push(chess.Move.from_uci(bestMoveDepth2))
        makeBoardMove(board, bestMoveDepth2)

        #print("turn: ", board.turn)

        #print("4_______")
        #print(board)

        scoreD2 = getScorePieces(board) * colorScoreCorrection


        resetBoard(board)


        if scoreD2 > bestScore:
            #print("setting new best move")
            bestScore = scoreD2
            bestMove = move



    #print("legal moves: ", legalMoves)
    #print("making move: ", bestMove)
    return bestMove






def getBestMoveDepth3(board):

    #print("iteration@@@@@@@@@@@@@@@@@@@@@@@@@")

    legalMoves = getLegalMoves(board)

    bestScore = -10000
    colorScoreCorrection = 1
    bestMove = ""

    if board.turn == chess.BLACK:
        colorScoreCorrection = -1

    for move in legalMoves:
        move = str(move)

        makeBoardMove(board, move)

        bestOpponentMove = getBestMoveDepth2(board)
        makeBoardMove(board, bestOpponentMove)


        bestMoveDepth2 = getBestMoveDepth2(board)
        makeBoardMove(board, bestMoveDepth2)

        bestOpponentMove2 = getBestMove1Depth(board)
        makeBoardMove(board, bestOpponentMove2)

        bestMoveDepth3 = getBestMove1Depth(board)
        makeBoardMove(board, bestMoveDepth3)


        scoreD3 = getScorePieces(board) * colorScoreCorrection


        resetBoard(board)


        if scoreD3 > bestScore:
            #print("setting new best move")
            bestScore = scoreD3
            bestMove = move



    #print("legal moves: ", legalMoves)
    #print("making move: ", bestMove)
    return bestMove

nWhiteWon = 0
nBlackWon = 0
nDraw = 0

getScorePieces(board)



for g in range(maxGames):

    board = chess.Board()

    savedGame = chess.pgn.Game()
    savedGame.headers["Event"] = "Example"

    node = None

    for m in range(maxMoves):

        # Check if game is over
        if board.is_stalemate():
            nDraw += 1
            break
        if board.is_game_over():

            result = board.result()
            if result == "1/2-1/2":
                nDraw += 1
            if result == "1-0":
                nWhiteWon += 1
            if result == "0-1":
                nBlackWon += 1

            savedGame.headers["Result"] = result

            break


        move = ""
        if board.turn == chess.WHITE:
            #move = getBestMove2Depthv3(board)
            move = getMoveRandom(board)
            #move = getBestMove2Depth(board)

        if board.turn == chess.BLACK:
            move = getBestMoveSearchTree(board, 1)
            #move = getBestMove3Depth(board)

        makeBoardMove(board, move)

        movesMade += 1

        #print("moves made: ", movesMade)

        #board.push(chess.Move.from_uci(move))

        print("trying move", move)

        if m == 0:
            node = savedGame.add_main_variation(chess.Move.from_uci(move))
        else:
            node = node.add_main_variation(chess.Move.from_uci(move))

        #node.comment = "value: " + str(getScorePieces(board))





    print("----------------------------------------------")
    print(str(savedGame))


if False:
    print(board)
    print("turn: ", board.turn)

    makeBoardMove(board, "e2e4")
    print(board)
    print("turn: ", board.turn)

    bestOpponentMove = getBestMove1Depth(board)
    makeBoardMove(board, bestOpponentMove)

    print(board)
    print("turn: ", board.turn)



if True:
    print("white won", nWhiteWon)
    print("black won", nBlackWon)
    print("draw", nDraw)
