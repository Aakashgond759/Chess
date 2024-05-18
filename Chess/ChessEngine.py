"""
    
 this class is responsible for storing all the information about the state of a chess game.
 it will also be responsible for determining the valid at the current state.
 it wil also keep a move log.
    
"""
class GameState():
    def __init__(self):
        # board is 8x8 2d list, each element of the list has 2 characters.
        # The first character represents the color of the piece, 'b' or 'w'
        # The second character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N' or 'P'
        # "--" represents an empty space with no piece.
        
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.WhiteToMove = True
        self.moveLog = []
        
    '''
    Takes a Move as a parameter and executes it ( this will not work for castling, pawn promotion and en-passant)
    '''    
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move so that we can undo it later
        self.WhiteToMove = not self.WhiteToMove # swap players
    

    '''undo the last move made'''
    def undoMove(self):
        if len(self.moveLog) != 0: # make sure taht there is  move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.WhiteToMove = not self.WhiteToMove # switch turns back
    
        """
        basic algorithm for getvalidmoves()
            - get all possible moves
            - generate all possible moves for the opposing player
            - see if any of the moves attack your king
            - if your king is safe, it is a valid move and add it to a list
        - retrun the list of valid moves only
            
        """
      
    # all mvess considering checks
     
    def getValidMoves(self):
        return self.getAllPossibleMoves() # for now we will not worry about checks
    
    
    # All moves without considerning checks
    
    def getAllPossibleMoves(self):
        moves = [Move((6,4), (4, 4), self.board)]
        for r in range(len(self.board)): # no of rows
            for c in range(len(self.board)): # no of columns in given rows
                turn = self.board[r][c][0]
                if (turn =='w' and self.WhiteToMove) and (turn == 'b' and not self.WhiteToMove):
                    piece = self.board[r][c][1]
                    if piece =='p':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves (r, c, moves)
        return moves          
            
        """
        get all the pawn moves for the pawn located at row, col and add these moves to the list
        """
    def getPawnMoves(self, r, c, moves):
        pass
    
    
    """
        get all the pawn moves for the Rook located at row, col and add these moves to the list
        """
    def getRookMoves(self, r, c, moves):
        pass
    
class Move():
    
    # maps keys to values
    # key : value
    
    ranksToRows = {
        "1":7, "2":6, "3":5, "4":4, 
        "5":3, "6":2, "7":1, "8":0
    }
    rowsToRanks = { v: k for k, v in ranksToRows.items() }
    
    filesToCols = {
        "a":0, "b":1, "c":2, "d":3,
        "e":4, "f":5, "g":6, "h":7
    }
    colsToFiles = { v: k for k, v in filesToCols.items() }
    
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol *100 + self.endRow *10 + self.endCol
        print("move ID =", self.moveID)
    
    '''
    overeiding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    