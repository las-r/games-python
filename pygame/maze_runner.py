import math
import pygame
import random

# 2.5d maze runner
# made by las-r on github
# v1.1

# init
pygame.init()
clk = pygame.time.Clock()
font = pygame.font.Font(None, 16)

# settings
WIDTH, HEIGHT = 800, 400
HW, HH = WIDTH // 2, HEIGHT // 2
MSIZE = 25
MJANK = 10
TSIZE = (WIDTH // 2) // MSIZE
FOVD = 70
FOV = (FOVD * math.pi) / 180
HFOV = FOV / 2
RAYS = 120
STEP = FOV / RAYS
MXDEPTH = 200

# colors
BGCOL = (0, 0, 0)
MZCOL = (255, 255, 255)
PLRCOL = (255, 0, 0)
LNCOL = (0, 255, 0)
RYCOL = (0, 255, 255)
TXCOL = (255, 0, 0)

# other constants
DIRS = [(-2, 0), (2, 0), (0, -2), (0, 2)]

# setup function
def setup():
    global px, py, pang, rspd, mspd, maze
    
    # player settings
    px = TSIZE + (TSIZE // 2)
    py = TSIZE // 2
    pang = 0.0
    rspd = 0.05
    mspd = 0.05 * TSIZE
    
    # maze generation
    maze = [[1 for _ in range(MSIZE)] for _ in range(MSIZE)]
    maze[0][1] = 0
    maze[-1][-2] = 0
    stk = []
    sy, sx = random.randrange(1, MSIZE, 2), random.randrange(1, MSIZE, 2)
    maze[sy][sx] = 0
    stk.append((sy, sx))
    while stk:
        y, x = stk[-1]
        random.shuffle(DIRS)
        moved = False
        for dy, dx in DIRS:
            ny, nx = y + dy, x + dx
            if 0 < ny < MSIZE - 1 and 0 < nx < MSIZE - 1 and maze[ny][nx] == 1:
                maze[y + dy // 2][x + dx // 2] = 0
                maze[ny][nx] = 0
                stk.append((ny, nx))
                moved = True
                break
        if not moved:
            stk.pop()
    for y in range(MSIZE):
        for x in range(MSIZE):
            if maze[y][x] and x not in (0, MSIZE - 1) and y not in (0, MSIZE - 1):
                if random.randint(1, MSIZE) < MSIZE * (MJANK / 100):
                    maze[y][x] = 0

# display
scr = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2.5D Maze Runner")

# setup
setup()

# other variables
text = False
noclip = False

# main loop
run = True
while run:
    # events
    for e in pygame.event.get():
        # quit event
        if e.type == pygame.QUIT:
            run = False
        
        # key events
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r:
                setup()
            if e.key == pygame.K_t:
                text = not text
            if e.key == pygame.K_n:
                noclip = not noclip
            
    # input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        pang = (pang - rspd) % (2 * math.pi)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        pang = (pang + rspd) % (2 * math.pi)
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        nx = px + math.cos(pang) * mspd
        ny = py + math.sin(pang) * mspd
        if not (0 < nx < TSIZE * MSIZE and 0 < ny < TSIZE * MSIZE):
            setup()
        if (not maze[int(ny / TSIZE)][int(nx / TSIZE)] or noclip):
            px, py = nx, ny
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        nx = px - math.cos(pang) * mspd
        ny = py - math.sin(pang) * mspd
        if (not maze[int(ny / TSIZE)][int(nx / TSIZE)] or noclip):
            px, py = nx, ny
    
    # draw maze
    scr.fill(BGCOL)
    for y in range(MSIZE):
        for x in range(MSIZE):
            if maze[y][x]:
                pygame.draw.rect(scr, MZCOL, (x * TSIZE, y * TSIZE, TSIZE - 1, TSIZE - 1))
                
    # draw rays
    sang = pang - HFOV
    for ray in range(RAYS):
        cosr, sinr = math.cos(sang), math.sin(sang)
        for depth in range(1, MXDEPTH * TSIZE, 2):
            tx = px + cosr * depth
            ty = py + sinr * depth
            gx, gy = int(tx / TSIZE), int(ty / TSIZE)
            if 0 <= gx < MSIZE and 0 <= gy < MSIZE:
                if maze[gy][gx]:
                    dist = depth * math.cos(sang - pang)
                    pygame.draw.line(scr, RYCOL, (px, py), (tx, ty))
                    wall_h = (TSIZE * 320) / (dist + 0.1)
                    c = 1 + dist * dist * (TSIZE / 16000)
                    pygame.draw.rect(scr, (MZCOL[0] // c, MZCOL[1] // c, MZCOL[2] // c), ( #type:ignore
                        HW + ray * (HW / RAYS), 
                        HH - wall_h // 2, 
                        (HW / RAYS) + 1, 
                        wall_h
                    ))
                    break
            else:
                break
        sang += STEP
    
    # draw player
    pygame.draw.circle(scr, PLRCOL, (int(px), int(py)), TSIZE // 2 - 4)
    pygame.draw.line(scr, LNCOL, (px, py), (px + math.cos(pang) * 40, py + math.sin(pang) * 40))
    
    # text
    if text:
        scr.blit(font.render(f"Player X: {round(px, 4)}", True, TXCOL), (5, 5))
        scr.blit(font.render(f"Player Y: {round(py, 4)}", True, TXCOL), (5, 20))
        scr.blit(font.render(f"Player angle: {round(pang * 180 / math.pi, 4)}", True, TXCOL), (5, 35))
        scr.blit(font.render(f"Noclip: {noclip}", True, TXCOL), (5, 50))
    
    # frame rate
    pygame.display.flip()
    clk.tick(60)
            
# quit
pygame.quit()
