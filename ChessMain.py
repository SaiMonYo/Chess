import ChessEngine
import pygame as p
import math
import random


width = height = 512
dim = 8 #Dimensions (8x8)
sqsize = height // dim
maxfps = 15
images = {} 

def loadImages():
    pieces = ["wP","wR","wN","wB","wQ","wK","bP","bR","bN","bB","bQ","bK"]
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/" + piece +".png"),(sqsize,sqsize))
        
def main():
    p.init()
    screen = p.display.set_mode((width,height))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))

    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True
    
    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                
            elif e.type == p.MOUSEBUTTONDOWN and gs.whiteToMove:
                location = p.mouse.get_pos()
                col = location[0]//sqsize
                row = location[1]//sqsize
                if sqSelected == (row,col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)
                    
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1], gs.board)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            
                    
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = True
        drawGameState(screen, gs)
        clock.tick(maxfps)
        p.display.flip()
                    
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        if gs.checkMate:
            print("Black wins by checkmate") if gs.whiteToMove else print("White wins by checkmate")
            running = False
        
        if gs.stalemate:
            print("Draw by stalemate")
            running = False

        if not gs.whiteToMove and len(validMoves) != 0 and not moveMade:
            move = gs.getBestMove(1)
            gs.makeMove(move)
            moveMade = True
            

def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colours = [p.Color("white"),p.Color("gray")]
    for r in range(dim):
        for c in range(dim):
            colour = colours[((r + c) % 2)]
            p.draw.rect(screen, colour, p.Rect(c*sqsize, r*sqsize, sqsize, sqsize))
            
            

def drawPieces(screen,board):
    for r in range(dim):
        for c in range(dim):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c*sqsize, r*sqsize, sqsize, sqsize))



if __name__ == "__main__":
    main()
