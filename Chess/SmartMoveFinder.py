import random
import ChessEngine, ChessMain

pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

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
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        opponentMaxScore = -CHECKMATE
        
        if gs.staleMate:
            opponentMaxScore = STALEMATE
        elif gs.checkMate:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentMove in opponentsMoves:
                gs.makeMove(opponentMove)
                #gs.getValidMoves() # uncomment this and it will make the moves for AI slower
                if gs.checkMate:
                    score = CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                    # bestPlayerMove = playerMove
                gs.undoMove()
        
        if  opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove 
        gs.undoMove()
    return bestPlayerMove
        

# helper method to make first recursive call
def findBestMoveMinMax(gs, validMoves):
    global nextMove
    nextMove = None
    findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    return nextMove


def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if DEPTH == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore
            
    

# a positive score is good for white, a negative score is good for black
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE # balck wins
        else:
            return CHECKMATE # white wins
    elif gs.staleMate:
        return STALEMATE
    
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score +=pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    
    return score


# score board based on material
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score +=pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    
    return score