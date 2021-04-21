import chess
import chess.pgn
import math
from collections.abc import Mapping
import json
from random import randrange


import berserk
import time
import itertools
client = berserk.Client()

upgradeToBot = False
if upgradeToBot:
    client.account.upgrade_to_bot()

token = ""

with open('.apitoken') as f:
    token = f.read().replace("\n", "")

session = berserk.TokenSession("" + token)
client = berserk.Client(session)

gameRunning = False
isWhite = True

board = chess.Board()
legalMoves = []

maxMoves = 1000
maxGames = 1


def getLegalMoves(board):
    legalMoves = []

    for move in board.legal_moves:
        legalMoves.append(str(move))
    return legalMoves


def split(word):
    return [char for char in word]


def isDict(variable):
    return isinstance(variable, Mapping)


def isEmptyDict(inDict):
    return not bool(inDict)


currentDepth = 0
movesMade = 0


def makeBoardMove(board, move):
    move = str(move)
    global currentDepth
    if move != "":
        newMove = chess.Move.from_uci(move)
        board.push(newMove)

        currentDepth += 1

    return board


def resetBoard(board):
    global currentDepth
    while currentDepth - movesMade != 0:
        board.pop()
        currentDepth -= 1


def resetBoardX(board, steps):
    global currentDepth

    for step in range(steps):
        if currentDepth - movesMade != 0:
            currentDepth -= 1
            board.pop()


def getScorePieces(board):
    chars = split(str(board))

    score = 0

    # make both players dont want to draw
    if board.is_stalemate():
        #print("HYPOTHETICAL STALEMATE")
        if board.turn == chess.WHITE:
            return -10
        else:
            return 10

    if board.can_claim_draw():
        # todo do min/max depending if below/over 0
        # print("CAN CLAIM DRAW")
        if board.turn == chess.WHITE:
            return -10
        else:
            return 10

    i = 0

    for char in chars:
        if char == ' ' or char == '\n':
            continue

        row = int(i/8)
        column = i % 8
        i += 1

        distanceToCenter = math.sqrt((row-3.5)**2 + (column-3.5)**2)

        positionValue = -(distanceToCenter/1000000.0)

        #print("distance", multiplier)

        # Black pieces
        if char == "r":
            score -= 5.63
            score -= positionValue
        elif char == "n":
            score -= 3.05
            score -= positionValue
        elif char == "q":
            score -= 9.5
        elif char == "b":
            score -= 3.33
            score -= positionValue
        elif char == "k":
            score -= 1000
            score += positionValue
        elif char == "p":
            score -= 1
            score -= positionValue

        # White pieces
        elif char == "R":
            score += 5.63
            score += positionValue
        elif char == "N":
            score += 3.05
            score += positionValue
        elif char == "Q":
            score += 9.5
        elif char == "B":
            score += 3.33
            score += positionValue
        elif char == "K":
            score += 1000
            score -= positionValue
        elif char == "P":
            score += 1
            score += positionValue

    # print(board)
    # print(score)

    return score


def getMoveRandom(board):
    legalMoves = getLegalMoves(board)
    #print("legal moves: ", len(legalMoves))

    moveIndex = randrange(0, len(legalMoves))
    return str(legalMoves[moveIndex])


def should_accept(arg):
    return not gameRunning


should_decline_if_in_game = True
for event in client.bots.stream_incoming_events():
    if event['type'] == 'challenge':
        print("event--------------------------------")
        print(event)
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

        if should_accept(event):
            client.bots.accept_challenge(event['challenge']['id'])
            gameID = event['challenge']['id']
            isWhite = event['challenge']['color'] == "black"

            print("starting challange")
            gameRunning = True
            break
        elif should_decline_if_in_game:
            client.bots.decline_challenge(event['challenge']['id'])
            print("declining challange")

print("done with loop")

# remove?
if not gameRunning:
    print("setting custom id @@@@@@@@@@@@@@@@@@@@@@")
    gameID = "vztNjpfq"

print("gameid: ", gameID)


def getMoveFirst(board):
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

        # board.push(chess.Move.from_uci(move))
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


def searchNode(board, node, moves, previousMoves, queue):
    minScore = 10000
    maxScore = -10000

    legalMoves = getLegalMoves(board)

    for move in legalMoves:
        #currentMoveTree[move] = {}

        score = getScoreAfterMove(board, move)
        #currentMoveTree[move][SCORE] = score
        #currentMoveTree[move][MOVES] = {}

        maxScore = max(maxScore, score)
        minScore = min(minScore, score)

        # propegate score upwards (TODO?)
        if board.turn == chess.WHITE:
            node["score"] = maxScore
        elif board.turn == chess.BLACK:
            node["score"] = minScore

        node["moves"][move] = {}

        node["moves"][move]["score"] = score
        node["moves"][move]["moves"] = {}

        #print("node: ", node)

        nextQueueMove = []

        nextQueueMove.extend(previousMoves)
        nextQueueMove.append(move)

        queue.insert(0, nextQueueMove)


def getBestMoveSearchTree(board, nNodes):

    bestMove = getMoveRandom(board)

    moves = {}
    searchedNodes = 0
    queue = []
    searchDepth = 0
    legalMoves = getLegalMoves(board)

    if len(legalMoves) == 0:
        return ""

    SCORE = "score"
    MOVES = "moves"

    for move in legalMoves:
        moves[move] = {}
        moves[move][SCORE] = getScoreAfterMove(board, move)
        moves[move][MOVES] = {}

    sortedMoves = sorted(moves.items(), key=lambda x: x[1][SCORE])

    for sortedMove in sortedMoves:

        if True:
            queue.append([sortedMove[0]])
        else:
            if board.turn == chess.WHITE:
                queue.append([sortedMove[0]])

            elif board.turn == chess.BLACK:
                queue.insert(0, [sortedMove[0]])

    #print("queue", queue)

    # always start from current board state
    while(searchedNodes < nNodes):
        searchedNodes += 1

        if len(queue) == 0:
            break

        queueMove = queue.pop()
        madeMoves = queueMove.copy()

        while len(queueMove) > 0:

            nextMove = queueMove.pop()
            if nextMove in getLegalMoves(board):
                searchDepth += 1

                if board.turn == chess.WHITE:
                    print("WHITE making move")
                else:
                    print("BLACK making move")

                print("move:", nextMove)

                makeBoardMove(board, nextMove)

                print(board)

                if False:
                    if board.turn == chess.WHITE:
                        #nextMove = sortedMoves[len(sortedMoves)-1][0]
                        nextMove = queue[len(sortedMoves)-1]

                    elif board.turn == chess.BLACK:
                        #nextMove = sortedMoves[0][0]
                        nextMove = queue[0]

                print("current Depth", searchDepth)

        print("queue popped:", madeMoves)

        prevMoveNode = moves[nextMove]
        #searchNode(board, prevMoveNode, moves, madeMoves, queue)

        #print("queue", queue)

        #moves[nextMove]["moves"] = currentMoveTree

        # board is reset to current state
        resetBoardX(board, searchDepth)
        searchDepth = 0

        #moves[move] = {}
        #moves[move][SCORE] = getScoreAfterMove(board, move)
        #moves[move][MOVES] = {}

        #print("actual moves", json.dumps(moves, indent= 4))
    #print("actual moves", json.dumps(moves, indent= 4))

    sortedMoves = sorted(moves.items(), key=lambda x: x[1][SCORE])

    bestMove = ""

    if board.turn == chess.WHITE:
        bestMove = sortedMoves[len(sortedMoves)-1][0]

    elif board.turn == chess.BLACK:
        bestMove = sortedMoves[0][0]

    #print("___________________RETURNING BEST MOVE__________________________")

    return str(bestMove)


def getBestMove2Depth(board):

    originalBoard = board.copy()

    legalMoves = getLegalMoves(board)

    bestScore = -10000
    colorScoreCorrection = 1
    bestMove = ""

    if board.turn == chess.BLACK:
        colorScoreCorrection = -1

    for move in legalMoves:
        move = str(move)
        board = originalBoard.copy()

        makeBoardMove(board, move)
        bestOpponentMove = getBestMove1Depth(board)
        makeBoardMove(board, bestOpponentMove)

        scoreD2 = getScorePieces(board) * colorScoreCorrection

        if scoreD2 > bestScore:
            bestScore = scoreD2
            bestMove = move

    board = originalBoard.copy()

    return bestMove


moves = {}

''' 
moveDepth
value
moves: []
isEvaluated
'''

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
        print("starting stuff")

        print("move: ", m)

        humanMove = ""

        if isWhite and m == 0:
            print("passing")
            client.bots.make_move(gameID, "e2e4")
            makeBoardMove(board, "e2e4")

        gen = client.bots.stream_game_state(gameID)

        breakLoop = False

        while not breakLoop:
            print("looping stuff 1")
            for element in gen:
                print("looping stuff")
                if(element):
                    if element['type'] == "gameState":
                        moves = element['moves'].split(" ")
                        humanMove = moves[len(moves)-1]

                        print("latest move: ")
                        print(humanMove)
                        makeBoardMove(board, humanMove)
                        print("made human move")
                        breakLoop = True
                        gen.close()

        print("doing normal stuff")
        if m % 10 == 0:
            print("move", m)

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
            move = getBestMove2Depth(board)
            #move = getBestMoveSearchTree(board, 2000)

        if board.turn == chess.BLACK:
            move = getBestMove2Depth(board)

        print("best move: ")
        print(move)

        makeBoardMove(board, move)
        client.bots.make_move(gameID, move)

        movesMade += 1
        print("made computer move")

        #print("moves made: ", movesMade)

        # board.push(chess.Move.from_uci(move))

        #print("trying move", move)

        if m == 0:
            node = savedGame.add_main_variation(chess.Move.from_uci(move))
        else:
            node = node.add_main_variation(chess.Move.from_uci(move))

        #node.comment = "value: " + str(getScorePieces(board))

    print("----------------------------------------------")
    print(str(savedGame))

if True:
    print("white won", nWhiteWon)
    print("black won", nBlackWon)
    print("draw", nDraw)
