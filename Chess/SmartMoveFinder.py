import random
import ChessEngine

pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0
'''
picks and returns a random move
'''
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

'''
find the best move
'''
def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    maxSCORE = -CHECKMATE
    bestMove = None
    
    if gs.checkMate:
        score = CHECKMATE
    elif gs.staleMate:
        score = STALEMATE
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        score = turnMultiplier * scoreMaterial(gs.board)
        if score > maxSCORE:
            maxSCORE = score  
            bestMove = playerMove
        gs.undoMove()
    return bestMove
        

'''
score board based on material
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score +=pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    
    return score