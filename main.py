import chess
import chess.pgn
from random import randrange

board = chess.Board()
legalMoves = []

maxMoves = 500
maxGames = 10

def getLegalMoves(board):
    legalMoves = []

    for move in board.legal_moves:
        legalMoves.append(move)
    return legalMoves

def split(word):
    return [char for char in word]

def getScorePieces(board):
    chars = split(str(board))

    score = 0

    for char in chars:

        # Black pieces
        if char == "r":
            score -= 5
        elif char == "n":
            score -= 2.9
        elif char == "q":
            score -= 9
        elif char == "b":
            score -= 3
        elif char == "k":
            score -= 1000
        elif char == "p":
            score -= 1

        # White pieces
        elif char == "R":
            score += 5
        elif char == "N":
            score += 2.9
        elif char == "Q":
            score += 9
        elif char == "B":
            score += 3
        elif char == "K":
            score += 1000
        elif char == "P":
            score += 1

    return score

def getMoveRandom(board):
    legalMoves = getLegalMoves(board)
    moveIndex = randrange(0, len(legalMoves))
    return str(legalMoves[moveIndex])


def getFirstMove(board):
    legalMoves = getLegalMoves(board)
    return str(legalMoves[0])

def getBestMove1Depth(board):
    legalMoves = getLegalMoves(board)

    bestMove = ""


    if board.turn == chess.WHITE:
        bestScore = -10000

        for move in legalMoves:
            move = str(move)

            board.push(chess.Move.from_uci(move))

            moveScore = getScorePieces(board)

            print("movescore: ", moveScore)

            if moveScore > bestScore:
                bestScore = moveScore
                bestMove = move

            # Reset board
            board.pop()

    if board.turn == chess.BLACK:
        bestScore = 10000

        for move in legalMoves:
            move = str(move)

            board.push(chess.Move.from_uci(move))

            moveScore = getScorePieces(board)

            print("movescore: ", moveScore)

            if moveScore < bestScore:
                bestScore = moveScore
                bestMove = move

            # Reset board
            board.pop()

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





        # Make moves
        legalMoves = getLegalMoves(board)
        move = ""
        if board.turn == chess.WHITE:
            move = getBestMove1Depth(board)
        if board.turn == chess.BLACK:
            move = getMoveRandom(board)

        board.push(chess.Move.from_uci(move))

        if m == 0:
            node = savedGame.add_main_variation(chess.Move.from_uci(move))
        else:
            node = node.add_main_variation(chess.Move.from_uci(move))



        # Game is over
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

            break


    print("----------------------------------------------")
    print(str(savedGame))



print("white won", nWhiteWon)
print("black won", nBlackWon)
print("draw", nDraw)
