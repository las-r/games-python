import pygame
import random

# minesweeper
# made by las-r on github
# v1.1

# init
pygame.init()
clk = pygame.time.Clock()
font = pygame.font.Font(None, 20)
largefont = pygame.font.Font(None, 70)
numfont = pygame.font.Font(None, 45)

# settings
WIDTH, HEIGHT = 1200, 640
BWIDTH, BHEIGHT = 30, 16
MINES = 99
TWIDTH, THEIGHT = WIDTH // BWIDTH, HEIGHT // BHEIGHT

# colors
BGCOL = (0, 0, 0)
COVERCOL = (96, 96, 96)
LINECOL = (255, 255, 255)
NUMCOLS = [
    (0, 0, 255),
    (0, 127, 0),
    (255, 0, 0),
    (127, 0, 255),
    (127, 0, 0),
    (0, 255, 255),
    (255, 255, 255),
    (255, 255, 0)
]
FLAGCOL = (255, 0, 0)
MINECOL = (255, 127, 0)
WINCOL = (0, 255, 0)
LOSECOL = (255, 0, 0)
DEBUGCOL = (0, 255, 255)

# text
WIN = largefont.render("You win!", True, WINCOL)
LOSE = largefont.render("You lose!", True, LOSECOL)
NUMS = [numfont.render(str(n + 1), True, NUMCOLS[n]) for n in range(8)]
FLAG = numfont.render("|>", True, FLAGCOL)

# helper variables
DIRS = [
    (0, 1),
    (1, 0),
    (1, 1),
    (0, -1),
    (-1, 0),
    (-1, -1),
    (-1, 1),
    (1, -1)
]

# helper functions
def breakAt(x, y):
    if (x, y) in flags:
        return
    tmines = getMines(x, y)
    tflags = getFlags(x, y)
    if (x, y) in uncovered:
        if tflags >= tmines:
            for dx, dy in DIRS:
                nx, ny = x + dx, y + dy
                if 0 <= nx < BWIDTH and 0 <= ny < BHEIGHT:
                    if (nx, ny) not in flags and (nx, ny) not in uncovered:
                        breakAt(nx, ny)
        return
    if not mines:
        while len(mines) < MINES:
            m = (random.randint(0, BWIDTH - 1), random.randint(0, BHEIGHT - 1))
            if m not in [(x, y)] + [(x + dx, y + dy) for dx, dy in DIRS]:
                mines.add(m)
    uncovered.add((x, y))
    if tmines == 0:
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < BWIDTH and 0 <= ny < BHEIGHT:
                breakAt(nx, ny)

def getMines(x, y):
    tmines = 0
    for dx, dy in DIRS:
        if (x + dx, y + dy) in mines:
            tmines += 1
    return tmines

def getFlags(x, y):
    tflags = 0
    for dx, dy in DIRS:
        if (x + dx, y + dy) in flags:
            tflags += 1
    return tflags

# display
scr = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

# game variables
uncovered = set()
flags = set()
mines = set()
state = ""
debug = False

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
            if not state:
                x, y = e.pos
                x //= TWIDTH
                y //= THEIGHT
                if e.button == 1:
                    breakAt(x, y)
                elif e.button == 3:
                    if (x, y) not in uncovered:
                        if (x, y) in flags:
                            flags.discard((x, y))
                        elif len(flags) < MINES:
                            flags.add((x, y))

        # key events
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_d:
                debug = not debug
            elif e.key == pygame.K_r:
                uncovered = set()
                flags = set()
                mines = set()
                state = ""
                
    # mouse pos
    mx, my = pygame.mouse.get_pos()
    tx, ty = mx // TWIDTH, my // THEIGHT

    # update game board
    scr.fill(BGCOL)
    for y in range(BHEIGHT):
        for x in range(BWIDTH):
            if (x, y) not in uncovered:
                pygame.draw.rect(scr, COVERCOL, pygame.Rect(x * TWIDTH, y * THEIGHT, TWIDTH, THEIGHT))
                if (x, y) in flags:
                    scr.blit(FLAG, FLAG.get_rect(center=(x * TWIDTH + TWIDTH // 2, y * THEIGHT + THEIGHT // 2)))
            else:
                tmines = getMines(x, y)
                if tmines:
                    nt = NUMS[tmines - 1]
                    scr.blit(nt, nt.get_rect(center=(x * TWIDTH + TWIDTH // 2, y * THEIGHT + THEIGHT // 2)))
            if state == "lose" or debug:
                if (x, y) in mines:
                    pygame.draw.ellipse(scr, MINECOL, pygame.Rect(x * TWIDTH, y * THEIGHT, TWIDTH, THEIGHT))
    for x in range(1, BWIDTH):
        pygame.draw.line(scr, LINECOL, (x * TWIDTH, 0), (x * TWIDTH, HEIGHT))
    for y in range(1, BHEIGHT):
        pygame.draw.line(scr, LINECOL, (0, y * THEIGHT), (WIDTH, y * THEIGHT))
    if debug:
        pygame.draw.rect(scr, DEBUGCOL, pygame.Rect(tx * TWIDTH, ty * THEIGHT, TWIDTH, THEIGHT), 2)

    # win/lose conditions
    if set(mines) & set(uncovered):
        state = "lose"
    if len(uncovered) == BWIDTH * BHEIGHT - MINES:
        state = "win"

    # text
    if debug:
        scr.blit(font.render(f"FPS: {clk.get_fps()}", True, DEBUGCOL), (5, 5))
        scr.blit(font.render(f"Flags: {flags}", True, DEBUGCOL), (5, 20))
        scr.blit(font.render(f"Mines: {mines}", True, DEBUGCOL), (5, 35))
        scr.blit(font.render(f"State: {state}", True, DEBUGCOL), (5, 50))
        scr.blit(font.render(f"Tile: {(tx, ty)}", True, DEBUGCOL), (5, 65))
        scr.blit(font.render(f"Mines around: {getMines(tx, ty)}", True, DEBUGCOL), (5, 80))
        scr.blit(font.render(f"Flags around: {getFlags(tx, ty)}", True, DEBUGCOL), (5, 95))
    if state == "win":
        scr.blit(WIN, WIN.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    if state == "lose":
        scr.blit(LOSE, LOSE.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

    # frame rate
    pygame.display.flip()
    clk.tick(60)

# quit
pygame.quit()
