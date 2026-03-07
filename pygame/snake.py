import pygame
import random

# snake
# made by las-r on github

# init
pygame.init()

# settings
W, H = 600, 600
BW, BH = 30, 30
TW, TH = W // BW, H // BH
SCOL = (0, 255, 0)
ACOL = (255, 0, 0)
BCOL = (0, 0, 0)

# helper functions
def reset():
    global snk, sdir, apl
    snk = [[BW // 3, BH // 2]]
    sdir = "right"
    apl = [2 * BW // 3, BH // 2]
def genApl():
    na = [random.randint(0, BW - 1), random.randint(0, BH - 1)]
    while na in snk:
        na = [random.randint(0, BW - 1), random.randint(0, BH - 1)]
    return na

# screen
scr = pygame.display.set_mode((W, H))
pygame.display.set_caption("Snake")

# set up game vars
snk = [[BW // 3, BH // 2]]
sdir = "right"
apl = [2 * BW // 3, BH // 2]

# game loop
run = True
while run:
    # input
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
            
        elif e.type == pygame.KEYDOWN:
            # movement
            if e.key in [pygame.K_w, pygame.K_UP] and sdir != "down": sdir = "up"
            elif e.key in [pygame.K_s, pygame.K_DOWN] and sdir != "up": sdir = "down"
            elif e.key in [pygame.K_a, pygame.K_LEFT] and sdir != "right": sdir = "left"
            elif e.key in [pygame.K_d, pygame.K_RIGHT] and sdir != "left": sdir = "right"
            
            # reset
            elif e.key == pygame.K_r: reset()
            
    # snake movement
    nh = snk[0].copy()
    if sdir == "up": nh[1] = (nh[1] - 1) % BH
    elif sdir == "down": nh[1] = (nh[1] + 1) % BH
    elif sdir == "left": nh[0] = (nh[0] - 1) % BW
    elif sdir == "right": nh[0] = (nh[0] + 1) % BW
    
    # death
    if nh in snk:
        pygame.time.delay(1000)
        reset()
        
    # apple
    if nh == apl: apl = genApl()
    else: snk.pop()
    
    # update head
    snk.insert(0, nh)
    
    # display
    scr.fill(BCOL)
    for s in snk:
        pygame.draw.rect(scr, SCOL, pygame.Rect(s[0] * TW, s[1] * TH, TW, TH))
    pygame.draw.rect(scr, ACOL, pygame.Rect(apl[0] * TW, apl[1] * TH, TW, TH))
    pygame.display.flip()
    
    # delay
    pygame.time.delay(75)
            
# quit
pygame.quit()
