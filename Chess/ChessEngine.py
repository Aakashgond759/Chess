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
        
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        # self.inCheck = False
        # self.pins = []
        # self.checks = []
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = () # coordinates for the square where en passant capture is possible
        self.currentCastlingRight = castleRights(True, True, True, True)
        self.castleRightsLog = [castleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                            self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)] 
        # self.castleRightsLog.append(self.currentCastlingRight)
    

    '''
    Takes a Move as a parameter and executes it ( this will not work for castling, pawn promotion and en-passant)
    '''    
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move so that we can undo it later
        self.whiteToMove = not self.whiteToMove # swap players
        # update the king's move if moved
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)
        
        # pawn promotion
        if move.pawnPromotion:
            promotedPiece = input("promoted to Q, R, B, or N: ")
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece
                
        # update enpassant possible vriable
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: # only on 2 square pwan advance
            #print("line 68", abs(move.startRow - move.endRow))
            self.enpassantPossible = ((move.endRow + move.startRow)//2, move.endCol)
            #print("en ", self.enpassantPossible)
        else:
            self.enpassantPossible = ()
        # enpassant move
        #print("line 74")
        #print(move.enPassant)
        if move.enPassant:
            self.board[move.startRow][move.endCol] = '--' # capturing the pawn
            #print("line 76", move.startRow, move.endCol)
        
        # castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: # kingside castle move
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1] # moves the rook 
                self.board[move.endRow][move.endCol + 1] = '--' # erase old rook
            else: # queenside castle move
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2] # moves the rook 
                self.board[move.endRow][move.endCol - 2] = '--'
        
        # update Castling rights - whenever it is a rook or a king move
        self.updateCastleRights(move)
        self.castleRightsLog.append(castleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                            self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))
                
           

    '''undo the last move made'''
    def undoMove(self):
        if len(self.moveLog) != 0: # make sure taht there is  move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # switch turns back
            # update the king's position if needed
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            # undo enpassant
            if move.enPassant:
                self.board[move.endRow][move.endCol] = '--' # remove the pawn that was added in the wrong square
                self.board[move.startRow][move.endCol] = move.pieceCaptured # puts the pawn on the correct square it was captured
                self.enpassantPossible = (move.endRow, move.endCol)  # allow an enpassant to happen on the next move
            # undo a 2 square pawn advance should make enpassantpissible = ()
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()      
            
            # undo castling rights   
            self.castleRightsLog.pop() # get rid of the new catle rights form the move we are undoing
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRight = castleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs) # set the current castle rights to the last one in the list
            
            # undo castel move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:  # king side castle
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else:  # queen side castle
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'
            
    
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: # left rook
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7: # right rook
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0 : # left rook
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7: # right rook
                    self.currentCastlingRight.bks = False
        
             
        """
        basic algorithm for getvalidmoves()
            - get all possible moves
            - generate all possible moves for the opposing player
            - see if any of the moves attack your king
            - if your king is safe, it is a valid move and add it to a list
        - retrun the list of valid moves only
            
        """  
        
    # all moves considering checks
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastelRights = castleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                            self.currentCastlingRight.wqs, self.currentCastlingRight.bqs) # copy the current castling rights
        #1. generate all possible moves
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        #2. for each move, make the move
        for i in range(len(moves)-1, -1, -1): # when removing from a list go backwards through that list
            self.makeMove(moves[i])
            #3. generate all opponent's moves
            #4. for each of your opponent's mves, see if they attack your king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i]) #5. if they do attach your king, not a valid move 
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
            
        if len(moves) == 0: # either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        
        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastelRights
        return moves
        #return self.getAllPossibleMoves() # for now we will not worry about checks
    
                        
    '''
    def getValidMoves(self):
        #tempEnpassantPossible = self.enpassantPossible
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        
        if self.inCheck:
            if len(self.checks) == 1: # only 1 check, block check or move king
                moves = self.getAllPossibleMoves()
                # to block a check you must move a piece into one of the squraes between the enemy piece and king
                check = self.checks[0] # check information
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] # enemy piece causing the block
                validSquares = [] # squares that pieces can move to 
                #if knight, must capture knight, other pieces can be blocked
                if pieceChecking[1] == "N":
                    validSquares=[(checkRow),(checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i) # check[2] and check [3] are the check directions
                        validSquares.append(validSquare)
                        if validSquares[0] == checkRow and validSquares[1] == checkCol:
                            # once you getto piece end checks
                            break
                # get rid of any moves then don't block check or move king
                for i in range(len(moves)-1, -1, -1): # gp thorugh backwards when you are removing from a list as iterating
                    if moves[i].pieceMoved[1] != 'K': # move doesn't move king so it must block or capture
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else: # double check, king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else: # not in check so all moves are fine
            moves = self.getAllPossibleMoves()
        
        #self.enpassantPossible = tempEnpassantPossible
        return moves           
        '''
        #22:52
    # determine if current player is in check
    
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])    
    
    # determine if the enemy can attack the square r, c
    
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove # switch to opponent's turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove # switch turns back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: # suqare is under attack
                return True
        return False
    
    
    # All moves without considerning checks
    
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): # no of rows
            for c in range(len(self.board)): # no of columns in given rows
                turn = self.board[r][c][0]
                if (turn =='w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
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
        piecePinned = False
        pinDirection = ()
        '''
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        '''
        if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            backRow=0
            enemyColor = 'b'
        else:
            moveAmount = 1 
            startRow = 1
            backRow = 7
            enemyColor = 'w'
        pawnPromotion = False
                    
        '''
        if self.whiteToMove: # white pwan moves
            if self.board[r-1][c]=="--": # 1 square pwan advance
                moves.append(Move((r, c), (r-1, c), self.board))
                if r==6 and self.board[r-2][c]=="--": #2 square pawn advance
                    moves.append(Move((r,c), (r-2, c),self.board))
        '''
            # new method pawn moves
        # old method
        '''
        if self.whiteToMove: # white pawn moves
            if self.board[r-1][c] =="--": # 1 square moved
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move( (r, c), (r-1, c), self.board))
                    if r == 6 and self.board[r-2][c] == '--': # 2 square moves
                        moves.append(Move((r, c), (r-2, c), self.board))
           
            #captures
            if c-1>=0: # captures to the left
                if self.board[r-1][c-1][0] =="b":  # enemies piece keys to capture
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r, c), (r-1, c-1), self.board))
                    elif (r-1)(c-1) == self.enPassant:
                        moves.append(Move((r, c), (r-1, c-1), self.board, enPassant=True))
            if c+1 <= 7: # captures to the right
                if self.board[r-1][c+1][0] == "b": # enemies piece to capture
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((r, c), (r-1, c+1), self.board))
                    elif (r-1)(c+1) == self.enPassant:
                        moves.append(Move((r, c), (r-1, c+1), self.board, enPassant=True))
        
        else: # black pawn moves
            if self.board[r+1][c] == "--": # 1 square move
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c), (r+1, c), self.board))        
                    if r==1 and self.board[r+2][c]=="--": # 2 square move
                        moves.append(Move((r, c), (r+2, c), self.board))
            # captures
            if c-1 >= 0: # capture to left
                if self.board[r+1][c-1][0] == "w":
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((r, c), (r+1, c-1), self.board))
                    elif (r+1)(c-1) == self.enPassant:
                        moves.append(Move((r, c), (r+1, c-1), self.board, enPassant=True))
            if c+1 <= 7: # capture to right
                if self.board[r+1][c+1][0] == "w":
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((r, c), (r+1, c+1), self.board))
                    elif (r+1)(c+1) == self.enPassant:
                        moves.append(Move((r, c), (r+1, c+1), self.board, enPassant=True))
        '''   
        #implement new move
        if self.board[r+moveAmount][c] == "--": # 1 square move
            if not piecePinned or pinDirection == (moveAmount, 0):
                #print("line 301")
                if r + moveAmount == backRow: # if piece gets to bank rank then it a pawn promotion
                    pawnPromotion = True
                moves.append(Move((r,c), (r + moveAmount, c), self.board, pawnPromotion = pawnPromotion))
                if r==startRow and self.board[r + 2 * moveAmount][c] == "--": # 2 square moves
                    moves.append(Move((r, c), (r + 2 * moveAmount, c), self.board))
        #  working
        if c-1>=0: # captures to left
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[r + moveAmount][c-1][0] == enemyColor: 
                    #print("line 310")
                    if r + moveAmount == backRow:# if piece gets to bank rank the it is a pwan promotion
                        pawnPromotion = True
                    moves.append(Move((r, c), (r + moveAmount, c-1), self.board, pawnPromotion = pawnPromotion))
                if ( r + moveAmount,  c-1) == self.enpassantPossible:
                    #print( "line 321", r+moveAmount, c-1)
                    moves.append(Move((r, c), (r + moveAmount, c-1), self.board, enPassant = True))
        # not working         
        if c+1<= 7 : # captures to right
            if not piecePinned or pinDirection == (moveAmount, 1):
                if self.board[r + moveAmount][c+1][0] == enemyColor: 
                    #print("line 322")
                    if r + moveAmount == backRow:# if piece gets to bank rank the it is a pwan promotion
                        pawnPromotion = True
                    moves.append(Move((r, c), (r + moveAmount, c+1), self.board, pawnPromotion = pawnPromotion))
                if ( r + moveAmount,  c+1) == self.enpassantPossible:
                    #print("line 332",r+moveAmount, c+1)
                    moves.append(Move((r, c), (r + moveAmount, c+1), self.board, enPassant = True))
            
    """
    get all the Rook moves for the Rook located at row, col and add these moves to the list
    """
    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        '''
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1]==c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q': # can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                    break
        '''
        directions = ( (-1, 0), (0, -1), (1, 0), (0, 1) ) # up, left, right, down
        enemyColor = "b" if self.whiteToMove else "w"
        
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
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
        piecePinned = False
        '''
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1]== c :
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        '''
        knightMoves = ( (-2, -1), (-2, 1),(-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1) )
        allyColor = "w" if self.whiteToMove else "b"
        
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0<= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: # not an ally piece (empty or enemy piece)
                        moves.append(Move((r, c), (endRow, endCol), self.board))
    
    """
    get all the Bishop moves for the Rook located at row, col and add these moves to the list
    """
    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        '''
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1]==c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        '''
        directions = ( (-1, -1), (-1, 1), (1, -1), (1, 1) ) #  diagonals
        enemyColor = "b" if self.whiteToMove else "w"
        
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece =="--": # empty space valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: # enemy piece valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else: # friendly piece invalid
                            break
                else: # off board
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
        #kingMoves = ( (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1) )
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            #endRow = r + kingMoves[i][0]
            #endCol = c + kingMoves[i][1]
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            
            if 0 <= endRow < 8 and 0 <= endCol< 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # not an ally piece (empty or empty piece)
                    # place king on and square and check for checks
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    #place king back on original loacation
                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)
        
        #self.getCastleMoves(r, c, moves, allyColor)
        
    # get all valid castle moves for the king at (r, c) and add them to the list of moves
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return # can't castle while we are in check
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)
        
    
    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove = True))
    
    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3]:
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove = True))
    
    
    def checkForPinsAndChecks(self):
        pins = [] # square where the allied pinned pece is and direction pinned from
        checks = [] # squares where enemy is applying a check
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            #print("black king")
            enemyColor = "w"
            allyColor = 'b'
            #print("ally color - ", allyColor)
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        # check outward from king for pins and check, keep track of pins
        directions = ( (-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1) ,(1, 1) )
        #print("inside checkForPinsAndChecks")
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () # reset possible pins
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                #print("inside i loop")
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    #print("endpiece - ", endPiece)
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == (): 
                            # list allied piece could be pinned                                            
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else: # 2nd allied piece, so no pin or check possible in this direction
                            break
                    elif endPiece[0] == enemyColor:
                        #print("ememy color got")
                        type = endPiece[1]
                        #print("inside elif after i loop: j = ", j)
                        # 5 possiblities here in this complex condition
                        # 1. orthogoally away from king and piece is a rook
                        # 2. diagonally away from king and piece is a bishop
                        # 3. 1 square away diagonally from king and piece is a pawn
                        # 4. any direction and piece is a queen
                        # 5. any direction 1 square away and piece is a king (this is necessary to revent a king move to a square controlled by anoter king)
                        if (0 <= j <= 3 and type == 'R' ) or ( 4 <= j <= 7 and type == 'B') or ( i == 1 and type =='p' and ((enemyColor == 'w' and 6 <= j <= 7 ) or (enemyColor == 'b' and 4 <= j <= 5) ) ) or (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == (): # no piece blocking, so check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                #print(inCheck)
                                break
                            else: # piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else: # enemy piece not applying check
                            break 
                else:
                    break # off board 
        # check for knight checks
        knightMoves = ((-2, -1), (-2, 1),(-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol <8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N': # enemy knight attacking king
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks
        
    ''' modified code
    def checkForPinsAndChecks(self):
        pins = []  # squares where allied pieces are pinned
        checks = []  # squares where enemy pieces are applying checks
        inCheck = False

        # Determine the side to move and their corresponding colors
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow, startCol = self.whiteKingLocation
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow, startCol = self.blackKingLocation

        # Directions for rook and queen (orthogonal) and bishop and queen (diagonal)
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for d in directions:
            possiblePin = ()  # reset possible pins
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    print(endPiece)
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:  # Second allied piece, no pin or check possible in this direction
                            break
                    elif endPiece[0] == enemyColor:
                        pieceType = endPiece[1]
                        if (0 <= directions.index(d) <= 3 and pieceType == 'R') or \
                        (4 <= directions.index(d) <= 7 and pieceType == 'B') or \
                        (i == 1 and pieceType == 'p' and ((enemyColor == 'w' and directions.index(d) in [6, 7]) or (enemyColor == 'b' and directions.index(d) in [4, 5]))) or \
                        (pieceType == 'Q') or (i == 1 and pieceType == 'K'):
                            if possiblePin == ():  # no piece blocking, so check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                            else:  # piece blocking so pin
                                pins.append(possiblePin)
                            break
                        else:  # enemy piece not applying check
                            break
                else:
                    break  # off the board

        # Check for knight checks
        knightMoves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':  # enemy knight attacking king
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))

        return inCheck, pins, checks
    '''

class castleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
    
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
    
    def __init__(self, startSq, endSq, board, pawnPromotion = False, enPassant = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol *100 + self.endRow *10 + self.endCol
        # pawn promotion
        self.pawnPromotion = pawnPromotion
        #if (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7):
        #    self.pawnPromotion = True
        # en passant
        self.enPassant = enPassant #(self.pieceMoved[1] == 'p' and (self.endRow, self.endCol) == enPassant)       
        if enPassant:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        # castle move
        self.isCastleMove = isCastleMove
        
    
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
    