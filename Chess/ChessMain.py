"""
this is our main driver file.
it will be responsible for handoling user input and displaying thr current GameState object.

"""
import pygame as p
import ChessEngine, SmartMoveFinder


WIDTH = HEIGHT = 512 # 400 is another option
DIMENSIONS = 8 # dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSIONS
MAX_FPS = 15 # for animation later on
IMAGES = {}

'''
initialize a global dictionary of images. this will be called excatly in the main
'''

def  loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("CHess/images/" + piece + ".png"), (SQ_SIZE,  SQ_SIZE))
        
    #IMAGES['bp'] = p.image.load("images/bp.png")
    # Note : we can access n image by saying 'IMAGES['wp']
    
    
'''
The main driver for our code. this will handle user input and udpating the graphics
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    
    #print(gs.board)
    
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable fpr when a move is made
    animate = False # flag vairable when we should animate a move
    
    loadImages()
    running = True
    sqSelected = () # no square is selected, keep track of the lasyt click of the user (tuple: (row, col))
    playerClicks = [] # this will keep tracks fo players click (two tuples: [(6, 4), (4, 4)])
    gameOver  = False
    
    '''
    playerone and playertwo, make both as True 
        - you can use for 2 player move
    playerone and playertwo, make anyone as True
        - you can play as white/black vs CPU
    playerone and playertwo, make both as False
        - you can let the CPU/AI to play for both
    '''
    playerOne = False # if a human is laying white, then this will be true, if an AI  is playing then its false 
    playerTwo = False # same as above but for black
    
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() #(x, y) location of mouse
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    
                    if sqSelected == (row, col): # the user clicked same square twice
                        sqSelected=() # deselector
                        playerClicks = [] # clear player clicks
                        
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) #append for both 1st and 2nd clicks
                                        
                    if len(playerClicks) == 2: # after 2nd click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade =True
                                animate = True
                                #gs.makeMove(move)
                                sqSelected = () # reset the user clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
                
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when z is pressed
                    gs.undoMove()
                    #validMoves = gs.getValidMoves()
                    moveMade = True
                    animate = False
                
                if e.key == p.K_r: # reset the board when r is pressed
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
        
        # AI move finder logic
        if not gameOver and not humanTurn:
            # to make it AI vs AI comment the next 2 line of code
            AIMove = SmartMoveFinder.findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = SmartMoveFinder.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True
                    
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
               
        drawGameState(screen, gs, validMoves, sqSelected)
        
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Balck wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate')
        
        
        clock.tick(MAX_FPS)
        p.display.flip()


'''
Highlight square select and moves for piece selected
'''
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected !=():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): # sqSelected ia a piece that can't be moved
            # higlight the seleted square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100 ) #transperency value -> 0 transparent; 255 opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color('green'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

    
'''
Responsible for all graphics within a current game state.
'''
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)  # draw squares on the board
    highlightSquares(screen, gs, validMoves, sqSelected)    
    drawPieces(screen, gs.board) # draw the pieces on top of those squares

'''
Draw the squares on the board, the top left square is always light
'''

def drawBoard(Screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color = colors[ (r+c) % 2  ]
            p.draw.rect(Screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
    
'''
Draw the pieces on the board using the current GameState.board
'''
    
def drawPieces(screen, board):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[r][c]
            if piece != "--": # not an empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def animateMove(move, screen, board, clock):
    global colors
    coords = [] # list of coordinates that the animation will move through
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSecond = 10 # frames move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSecond
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw the moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Arial", 36, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)  
    textObject = font.render(text, 0, p.Color("Gray"))
    screen.blit(textObject, textLocation.move(2, 2))

if __name__ == "__main__":
    main()