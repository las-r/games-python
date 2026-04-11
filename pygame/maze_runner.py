import math
import pygame

# 2.5d maze runner
# made by las-r on github

# init
pygame.init()
clk = pygame.time.Clock()
font = pygame.font.Font(None, 16)

# settings
WIDTH, HEIGHT = 800, 400
HW, HH = WIDTH // 2, HEIGHT // 2

MSIZE = 8
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

# player settings
px = 200.0
py = 200.0
pang = 0.0
rspd = 0.05
mspd = 3.0

# map
MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]

# display
scr = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2.5D Maze Runner")

# main loop
run = True
while run:
    # events
    for e in pygame.event.get():
        # quit event
        if e.type == pygame.QUIT:
            run = False
            
    # input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        pang -= rspd
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        pang += rspd
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        nx = px + math.cos(pang) * mspd
        ny = py + math.sin(pang) * mspd
        if not MAP[int(ny / TSIZE)][int(nx / TSIZE)]:
            px, py = nx, ny
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        nx = px - math.cos(pang) * mspd
        ny = py - math.sin(pang) * mspd
        if not MAP[int(ny / TSIZE)][int(nx / TSIZE)]:
            px, py = nx, ny
    
    # draw map
    scr.fill(BGCOL)
    for y in range(MSIZE):
        for x in range(MSIZE):
            if MAP[y][x]:
                pygame.draw.rect(scr, MZCOL, (x * TSIZE, y * TSIZE, TSIZE - 1, TSIZE - 1))
                
    # draw rays
    sang = pang - HFOV
    for ray in range(RAYS):
        cosr, sinr = math.cos(sang), math.sin(sang)
        for depth in range(1, MXDEPTH * TSIZE, 2):
            tx = px + cosr * depth
            ty = py + sinr * depth
            if MAP[int(ty / TSIZE)][int(tx / TSIZE)]:
                dist = depth * math.cos(sang - pang)
                pygame.draw.line(scr, RYCOL, (px, py), (tx, ty))
                wall_h = (TSIZE * 320) / (dist + 0.1)
                c = 1 + dist * dist * 0.0005
                pygame.draw.rect(scr, (MZCOL[0] // c, MZCOL[1] // c, MZCOL[2] // c), ( # type: ignore
                    HW + ray * (HW / RAYS), 
                    HH - wall_h // 2, 
                    (HW / RAYS) + 1, 
                    wall_h
                ))
                break
        sang += STEP
    
    # draw player
    pygame.draw.circle(scr, PLRCOL, (int(px), int(py)), 12)
    pygame.draw.line(scr, LNCOL, (px, py), (px + math.cos(pang) * 40, py + math.sin(pang) * 40))
    
    # text
    scr.blit(font.render(f"Player X: {round(px, 4)}", True, TXCOL), (5, 5))
    scr.blit(font.render(f"Player Y: {round(py, 4)}", True, TXCOL), (5, 20))
    scr.blit(font.render(f"Player angle: {round((pang * 180 / math.pi) % 360, 4)}", True, TXCOL), (5, 35))
    
    # frame rate
    pygame.display.flip()
    clk.tick(60)
            
# quit
pygame.quit()
