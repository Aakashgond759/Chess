"""
this is our main driver file.
it will be responsible for handoling user input and displaying thr current GameState object.

"""
import pygame as p
import ChessEngine


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
    
    loadImages()
    running = True
    sqSelected = () # no square is selected, keep track of the lasyt click of the user (tuple: (row, col))
    playerClicks = [] # this will keep tracks fo players click (two tuples: [(6, 4), (4, 4)])
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x, y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                sqSelected = (row, col)
                if sqSelected == (row, col): # the user clicked same square twice
                    
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
    
'''
Responsible for all graphics within a current game state.
'''
def drawGameState(screen, gs):
    drawBoard(screen)  # draw squares on the board
    #add in piece highlighting or move suggestions     
    drawPieces(screen, gs.board) # draw the pieces on top of those squares

'''
Draw the squares on the board, the top left square is always light
'''

def drawBoard(Screen):
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



if __name__ == "__main__":
    main()