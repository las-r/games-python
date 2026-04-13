import math
import pygame
import random

# 2.5d maze runner
# made by las-r on github
# v1.3

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
MXDEPTH = 200
FALLOFF = 0.5

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
text = True
noclip = False
fisheye = False
rays = WIDTH // 2
fovd = 70
fov = (fovd * math.pi) / 180
hfov = fov / 2
step = fov / rays

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
            elif e.key == pygame.K_f:
                pang += math.pi
            elif e.key == pygame.K_t:
                text = not text
            elif e.key == pygame.K_1:
                noclip = not noclip
            elif e.key == pygame.K_2:
                fisheye = not fisheye
            
    # player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        pang = (pang - rspd) % (2 * math.pi)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        pang = (pang + rspd) % (2 * math.pi)
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        dx = math.cos(pang) * mspd
        dy = math.sin(pang) * mspd
        nx = px + dx
        if not maze[int(py / TSIZE)][int(nx / TSIZE)] or noclip:
            px = nx
        ny = py + dy
        if not maze[int(ny / TSIZE)][int(px / TSIZE)] or noclip:
            py = ny
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        dx = -math.cos(pang) * mspd
        dy = -math.sin(pang) * mspd
        nx = px + dx
        if not maze[int(py / TSIZE)][int(nx / TSIZE)] or noclip:
            px = nx
        ny = py + dy
        if not maze[int(ny / TSIZE)][int(px / TSIZE)] or noclip:
            py = ny
    px = max(TSIZE, min((MSIZE - 1) * TSIZE, px))
    py = max(0, min((MSIZE - 1) * TSIZE, py))
    
    # fov changing
    if keys[pygame.K_MINUS]:
        fovd -= 1
        fov = (fovd * math.pi) / 180
        hfov = fov / 2
        step = fov / rays
    if keys[pygame.K_EQUALS]:
        fovd += 1
        fov = (fovd * math.pi) / 180
        hfov = fov / 2
        step = fov / rays
        
    # rays changing
    if keys[pygame.K_COMMA]:
        rays -= 1
        step = fov / rays
    if keys[pygame.K_PERIOD]:
        rays += 1
        step = fov / rays
    
    # draw maze
    scr.fill(BGCOL)
    for y in range(MSIZE):
        for x in range(MSIZE):
            if maze[y][x]:
                pygame.draw.rect(scr, MZCOL, (x * TSIZE, y * TSIZE, TSIZE - 1, TSIZE - 1))
                
    # draw rays
    sang = pang - hfov
    for ray in range(rays):
        cosr = math.cos(sang)
        sinr = math.sin(sang)
        deltax = abs(1 / cosr) if cosr != 0 else 1e30
        deltay = abs(1 / sinr) if sinr != 0 else 1e30
        mapx = int(px / TSIZE)
        mapy = int(py / TSIZE)
        if cosr < 0:
            stepx = -1
            sidedistx = (px / TSIZE - mapx) * deltax
        else:
            stepx = 1
            sidedistx = (mapx + 1.0 - px / TSIZE) * deltax
        if sinr < 0:
            stepy = -1
            sidedisty = (py / TSIZE - mapy) * deltay
        else:
            stepy = 1
            sidedisty = (mapy + 1.0 - py / TSIZE) * deltay
        hit = 0
        side = 0
        while hit == 0:
            if sidedistx < sidedisty:
                sidedistx += deltax
                mapx += stepx
                side = 0
            else:
                sidedisty += deltay
                mapy += stepy
                side = 1
            if 0 <= mapx < MSIZE and 0 <= mapy < MSIZE:
                if maze[mapy][mapx] > 0:
                    hit = 1
            else:
                break
        if side == 0:
            perpdist = (sidedistx - deltax)
        else:
            perpdist = (sidedisty - deltay)
        dist = perpdist * TSIZE
        tx = px + cosr * dist
        ty = py + sinr * dist
        pygame.draw.line(scr, RYCOL, (px, py), (tx, ty))
        if fisheye:
            correctdist = dist
        else:
            correctdist = dist * math.cos(sang - pang)
        wallh = (TSIZE * 300) / (correctdist + 0.1)
        brightness = 1 / (1 + (perpdist * perpdist * FALLOFF))
        color = (MZCOL[0] * brightness, MZCOL[1] * brightness, MZCOL[2] * brightness)
        pygame.draw.rect(scr, color, ( #type:ignore
            HW + ray * (HW / rays), 
            HH - wallh // 2, 
            (HW / rays) + 1, 
            wallh
        ))
        sang += step
    
    # draw player
    pygame.draw.circle(scr, PLRCOL, (int(px), int(py)), TSIZE // 2 - 4)
    pygame.draw.line(scr, LNCOL, (px, py), (px + math.cos(pang) * 40, py + math.sin(pang) * 40))
    
    # text
    if text:
        scr.blit(font.render(f"Player X: {round(px, 4)}", True, TXCOL), (HW + 5, 5))
        scr.blit(font.render(f"Player Y: {round(py, 4)}", True, TXCOL), (HW + 5, 20))
        scr.blit(font.render(f"Player angle: {round(pang * 180 / math.pi, 4)}", True, TXCOL), (HW + 5, 35))
        scr.blit(font.render(f"FOV: {fovd}", True, TXCOL), (HW + 5, 50))
        scr.blit(font.render(f"Noclip: {noclip}", True, TXCOL), (HW + 5, 65))
        scr.blit(font.render(f"Fisheye distortion: {fisheye}", True, TXCOL), (HW + 5, 80))
        scr.blit(font.render(f"Rays: {rays}", True, TXCOL), (HW + 5, 95))
    
    # frame rate
    pygame.display.flip()
    clk.tick(60)
            
# quit
pygame.quit()
