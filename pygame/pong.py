import pygame
import random

# two player pong
# made by las-r on github

# init
pygame.init()
clk = pygame.time.Clock()
font = pygame.font.Font(None, 40)

# settings
WIDTH, HEIGHT = 800, 600
P1X, P2X = 60, WIDTH - 60
PSPEED = 20
PSIZE = (12, 120)
BSTARTSPEED = 6
BSIZE = 30
P1STX, P1STY = 120, 50
P2STX, P2STY = WIDTH - 120, 50

# colors
BGCOL = (0, 0, 0)
PCOL = (255, 255, 255)
BCOL = (255, 255, 255)
TCOL = (255, 255, 255)

# other constants
PHBX = PSIZE[0] // 2
PHBY = PSIZE[1] // 2
BHB = BSIZE // 2

# helper functions
def reset():
    global p1, p2, bx, by, bdx, bdy, bspeed
    p1 = HEIGHT // 2
    p2 = HEIGHT // 2
    bx, by = WIDTH // 2, HEIGHT // 2
    bdx, bdy = random.choice([-1, 1]), random.choice([-1, 1])
    bspeed = BSTARTSPEED

# display
scr = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# game values
p1 = HEIGHT // 2
p2 = HEIGHT // 2
bx, by = WIDTH // 2, HEIGHT // 2
bdx, bdy = random.choice([-1, 1]), random.choice([-1, 1])
bspeed = BSTARTSPEED
p1s = 0
p2s = 0
bp = False

# game loop
run = True
while run:
    # events
    for e in pygame.event.get():
        # quit event
        if e.type == pygame.QUIT:
            run = False
                
    # player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        p1 = max(PHBY, min(HEIGHT - PHBY, p1 - PSPEED))
    elif keys[pygame.K_s]:
        p1 = max(PHBY, min(HEIGHT - PHBY, p1 + PSPEED))
    if keys[pygame.K_UP]:
        p2 = max(PHBY, min(HEIGHT - PHBY, p2 - PSPEED))
    elif keys[pygame.K_DOWN]:
        p2 = max(PHBY, min(HEIGHT - PHBY, p2 + PSPEED))
        
    # game logic
    bx += bdx * bspeed
    by += bdy * bspeed
    if not BHB <= by <= HEIGHT - BHB:
        bdy = -bdy
    if P1X - PHBX - BHB <= bx <= P1X + PHBX + BHB and p1 - PHBY <= by <= p1 + PHBY:
        if not bp:
            bdx = -bdx
            bspeed += 1
            bp = True
    elif P2X + PHBX + BHB >= bx >= P2X - PHBX - BHB and p2 - PHBY <= by <= p2 + PHBY:
        if not bp:
            bdx = -bdx
            bspeed += 1
            bp = True
    else:
        bp = False
    if bx <= BHB:
        p2s += 1
        pygame.time.wait(1000)
        reset()
    elif bx >= WIDTH - BHB:
        p1s += 1
        pygame.time.wait(1000)
        reset()
        
    # update screen
    scr.fill(BGCOL)
    p1r = pygame.Rect(0, 0, PSIZE[0], PSIZE[1])
    p1r.center = (P1X, p1)
    pygame.draw.rect(scr, PCOL, p1r)
    p2r = pygame.Rect(0, 0, PSIZE[0], PSIZE[1])
    p2r.center = (P2X, p2)
    pygame.draw.rect(scr, PCOL, p2r)
    br = pygame.Rect(0, 0, BSIZE, BSIZE)
    br.center = (bx, by)
    pygame.draw.ellipse(scr, BCOL, br)
    
    # text
    scr.blit(font.render(str(p1s), True, TCOL), (P1STX, P1STY))
    scr.blit(font.render(str(p2s), True, TCOL), (P2STX, P2STY))
            
    # frame rate
    pygame.display.flip()
    clk.tick(60)

# quit
pygame.quit()
