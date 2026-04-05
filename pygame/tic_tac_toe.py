import pygame

# 2 player tic tac toe
# made by las-r on github

# init
pygame.init()
clk = pygame.time.Clock()
font = pygame.font.Font()
xofont = pygame.font.Font(None, 90)

# settings
WIDTH, HEIGHT = 600, 600
TWIDTH, THEIGHT = WIDTH // 3, HEIGHT // 3
HTW, HTH = TWIDTH // 2, THEIGHT // 2

# colors
BGCOL = (0, 0, 0)
LNCOL = (255, 255, 255)
TXCOL = (0, 255, 255)
XCOL = (255, 0, 0)
OCOL = (0, 0, 255)

# pretext
X = xofont.render("X", True, XCOL)
O = xofont.render("O", True, OCOL)
XWIN = xofont.render("X won!", True, TXCOL)
OWIN = xofont.render("O won!", True, TXCOL)
DRAW = xofont.render("Draw!", True, TXCOL)

# helpers
def getPos(x, y):
    return board[y][x]

def checkWin():
    global win
    lines = [
        [(0,0),(1,0),(2,0)],
        [(0,1),(1,1),(2,1)],
        [(0,2),(1,2),(2,2)],
        [(0,0),(0,1),(0,2)],
        [(1,0),(1,1),(1,2)],
        [(2,0),(2,1),(2,2)],
        [(0,0),(1,1),(2,2)],
        [(2,0),(1,1),(0,2)]
    ]
    for l in lines:
        if getPos(*l[0]) and getPos(*l[0]) == getPos(*l[1]) == getPos(*l[2]):
            win = getPos(*l[0])
            start = l[0]
            end = l[2]
            return (start[0] * TWIDTH + HTW, start[1] * THEIGHT + HTH), (end[0] * TWIDTH + HTW, end[1] * THEIGHT + HTH)
    return None, None

# display
scr = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# game vars
board = [["" for _ in range(3)] for _ in range(3)]
turn = "x"
win = ""

# game loop
run = True
while run:
    # events
    for e in pygame.event.get():
        # quit event
        if e.type == pygame.QUIT:
            run = False
            
        # mouse events
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                if not win:
                    mx, my = e.pos
                    tx, ty = mx // TWIDTH, my // THEIGHT
                    if not board[ty][tx]:
                        board[ty][tx] = turn
                        if turn == "x":
                            turn = "o"
                        elif turn == "o":
                            turn = "x"
                            
        # key events
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r:
                board = [["" for _ in range(3)] for _ in range(3)]
                turn = "x"
                win = ""
                
    # check win
    if not win:
        wstart, wend = checkWin()
    if not win and all(item != "" for row in board for item in row):
        win = "draw"
            
    # update display
    scr.fill(BGCOL)
    for x in range(1, 3):
        pygame.draw.line(scr, LNCOL, (x * TWIDTH, 0), (x * TWIDTH, HEIGHT), 2)
    for y in range(1, 3):
        pygame.draw.line(scr, LNCOL, (0, y * THEIGHT), (WIDTH, y * THEIGHT), 2)
    for y in range(3):
        for x in range(3):
            if board[y][x] == "x":
                scr.blit(X, X.get_rect(center=(x * TWIDTH + HTW, y * THEIGHT + HTH)))
            elif board[y][x] == "o":
                scr.blit(O, O.get_rect(center=(x * TWIDTH + HTW, y * THEIGHT + HTH)))
                
    # text
    scr.blit(font.render(f"Turn: {turn}", True, TXCOL), (5, 5))
    if win == "x":
        pygame.draw.line(scr, XCOL, wstart, wend, 10) #type: ignore
        scr.blit(XWIN, XWIN.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    elif win == "o":
        pygame.draw.line(scr, OCOL, wstart, wend, 10) #type: ignore
        scr.blit(OWIN, OWIN.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    elif win == "draw":
        scr.blit(DRAW, DRAW.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            
    # frame rate
    pygame.display.flip()
    clk.tick(60)
            
# quit
pygame.quit()
