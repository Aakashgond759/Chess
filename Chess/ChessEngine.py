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

        self.moveFunctions = {
            "p" : self.getPawnMoves,
            "R" : self.getRookMoves,
            "N" : self.getKnightsMoves,
            "B" : self.getBishopMoves,
            "Q" : self.getQueenMoves,
            "K" : self.getKingMoves
        }
        
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
        moves = []
        for r in range(len(self.board)): # no of rows
            for c in range(len(self.board)): # no of columns in given rows
                turn = self.board[r][c][0]
                if (turn =='w' and self.WhiteToMove) or (turn == 'b' and not self.WhiteToMove):
                    piece = self.board[r][c][1]
                    '''if piece =='p':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves (r, c, moves)'''
                    self.moveFunctions[piece](r, c, moves) # calls the appropriate oves function
                    
        return moves          
            
        """
        get all the pawn moves for the pawn located at row, col and add these moves to the list
        """
    def getPawnMoves(self, r, c, moves):
        if self.WhiteToMove: # white pwan moves
            if self.board[r-1][c]=="--": # 1 square pwan advance
                moves.append(Move((r, c), (r-1, c), self.board))
                if r==6 and self.board[r-2][c]=="--": #2 square pawn advance
                    moves.append(Move((r,c), (r-2, c),self.board))
            #captures
            if c-1>=0: # captures to the left
                if self.board[r-1][c-1][0] =="b":  # enemies piece keys to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            
            if c+1 <= 7: # captures to the right
                if self.board[r-1][c+1][0] == "b": # enemies piece to capture
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        
        else: # black pawn moves
            if self.board[r+1][c] == "--": # 1 square move
                moves.append(Move((r, c), (r+1, c), self.board))        
                if r==1 and self.board[r+2][c]=="--": # 2 square move
                    moves.append(Move((r, c), (r+2, c), self.board))
            # captures
            if c-1 >= 0: # capture to left
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                
            if c+1 <= 7: # capture to right
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r, c), (r+1, c+1), self.board))
    
    """
    get all the Rook moves for the Rook located at row, col and add these moves to the list
    """
    def getRookMoves(self, r, c, moves):
        directions = ( (-1, 0), (0, -1), (1, 0), (0, 1) ) # up, left, right, down
        enemyColor = "b" if self.WhiteToMove else "w"
        
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: # friendly piece invalid
                        break
                else: # off board
                    break  
    
    """
    get all the Kinghts moves for the Rook located at row, col and add these moves to the list
    """
    def getKnightsMoves(self, r, c, moves):
        knightMoves = ( (-2, -1), (-2, 1),(-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1) )
        allyColor = "w" if self.WhiteToMove else "b"
        
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            
            if 0<= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # not an ally piece (empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))
    
    """
    get all the Bishop moves for the Rook located at row, col and add these moves to the list
    """
    def getBishopMoves(self, r, c, moves):
        directions = ( (-1, -1), (-1, 1), (1, -1), (1, 1) ) #  diagonals
        enemyColor = "b" if self.WhiteToMove else "w"
        
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece =="--": # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
    
    """
    get all the Queen moves for the Rook located at row, col and add these moves to the list
    """
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
        
    
    """
    get all the King moves for the Rook located at row, col and add these moves to the list
    """
    def getKingMoves(self, r, c, moves):
        kingMoves = ( (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1) )
        allycolor = "w" if self.WhiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            
            if 0 <= endRow < 8 and 0 <= endCol< 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allycolor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
    
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
        #print("move ID =", self.moveID)
    
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
    