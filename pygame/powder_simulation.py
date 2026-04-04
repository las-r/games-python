import ptext
import pygame
import random

# powder simulation
# made by las-r on github
# v1.2

# THIS REQUIRES A LIBRARY `ptext.py`:
# https://github.com/cosmologicon/pygame-text/blob/master/ptext.py

# init pygame
pygame.init()
clk = pygame.time.Clock()

# settings
DW, DH = 800, 600
GW, GH = 100, 75
TW, TH = DW // GW, DH // GH

# functions
def getSur(x, y):
    result = []
    for dx, dy in [(-1, -1), (0, -1), (1, -1), (-1,  0), (1,  0), (-1,  1), (0,  1), (1,  1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GW and 0 <= ny < GH:
            result.append(box[ny][nx])
    return result

# elements behavior
def powder(x, y, fineness):
    if "z" not in getSur(x, y):
        if y + 1 < GH and not box[y + 1][x]:
            return x, y + 1
        dirs = [-1, 1]
        random.shuffle(dirs)
        if random.random() < fineness:
            for dx in dirs:
                nx, ny = x + dx, y + 1
                if 0 <= nx < GW and ny < GH and (not box[ny][nx] and not box[ny - 1][nx]):
                    return nx, ny
        return x, y
def liquid(x, y, viscosity):
    if "z" not in getSur(x, y):
        if y + 1 < GH and not box[y + 1][x]:
            return x, y + 1
        ddirs = [-1, 1]
        random.shuffle(ddirs)
        if random.random() < viscosity:
            for dx in ddirs:
                nx, ny = x + dx, y + 1
                if 0 <= nx < GW and ny < GH and (not box[ny][nx] and not box[ny - 1][nx]):
                    return nx, ny
        sdirs = [-1, 1]
        random.shuffle(sdirs)
        if random.random() < viscosity:
            for sx in sdirs:
                nx, ny = x + sx, y
                if 0 <= nx < GW and ny < GH and (not box[ny][nx] and not box[ny - 1][nx]):
                    return nx, ny
        return x, y
def solid(x, y, z):
    if "z" not in getSur(x, y):
        if y + 1 < GH:
            return x, y + 1
        return x, y
def metal(x, y, z):
    return x, y

# elements database
ELE = {
    # powders
    "1": {"nm": "Sand", "col": (232, 218, 111), "bhvr": powder, "arg": 0.6, "ds": 3},
    "2": {"nm": "Rocks", "col": (91, 91, 91), "bhvr": powder, "arg": 0.05, "ds": 5},
    "3": {"nm": "Dirt", "col": (79, 37, 22), "bhvr": powder, "arg": 0.18, "ds": 4},
    "0": {"nm": "Gamowder", "col": "rand", "bhvr": powder, "arg": 1, "ds": 0},
    
    # liquids
    "q": {"nm": "Water", "col": (35, 69, 150), "bhvr": liquid, "arg": 0.76, "ds": 1},
    "w": {"nm": "Honey", "col": (235, 172, 47), "bhvr": liquid, "arg": 0.12, "ds": 3.2},
    "e": {"nm": "Oil", "col": (232, 231, 202), "bhvr": liquid, "arg": 1, "ds": 0.7},
    "t": {"nm": "Milk", "col": (255, 255, 255), "bhvr": liquid, "arg": 0.43, "ds": 1.7},
    "p": {"nm": "Gamiquid", "col": "rand", "bhvr": liquid, "arg": 1, "ds": 0},
    
    # solids
    "a": {"nm": "Stone", "col": (130, 130, 130), "bhvr": solid, "ds": 11},
    "l": {"nm": "Gamolid", "col": "rand", "bhvr": solid, "ds": 0},
    
    # metals
    "n": {"nm": "Steel", "col": (28, 28, 28), "bhvr": metal, "ds": 100},
    "m": {"nm": "Gametal", "col": "rand", "bhvr": metal, "ds": 0},
    
    # misc
    "": {"nm": "Air", "col": (0, 0, 0), "bhvr": metal, "ds": 0},
    "z": {"nm": "Void", "col": "semirand 10 10 10 5", "bhvr": metal, "ds": 0},
}

# variables
psd = True
spd = 60
box = [["" for _ in range(GW)] for _ in range(GH)]
selTl = "1"
brush = 1

# display
scr = pygame.display.set_mode((DW, DH))
pygame.display.set_caption("Powder Simulation")

# main loop
run = True
while run:
    for e in pygame.event.get():
        # quit
        if e.type == pygame.QUIT:
            run = False
            
        # key
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                psd = not psd
            elif e.key == pygame.K_r:
                box = [["" for _ in range(GW)] for _ in range(GH)]
            elif e.key == pygame.K_UP:
                brush = max(0, min(brush + 1, 12))
            elif e.key == pygame.K_DOWN:
                brush = max(0, min(brush - 1, 12))
            else:
                k = pygame.key.name(e.key)
                if k in ELE:
                    selTl = k
                    
        # scroll
        elif e.type == pygame.MOUSEWHEEL:
            spd = max(2, min(spd + e.y, 240))
            
    # draw element tiles
    mb = pygame.mouse.get_pressed()
    mx, my = pygame.mouse.get_pos()
    mgx, mgy = mx // TW % GW, my // TH % GH
    if any(mb):
        if mb[0]:
            for by in range(-brush, brush + 1):
                for bx in range(-brush, brush + 1):
                    nx, ny = mgx + bx, mgy + by
                    if 0 <= nx < GW and 0 <= ny < GH:
                        box[ny][nx] = selTl
        if mb[1]:
            if box[mgy][mgx]:
                selTl = box[mgy][mgx]
        if mb[2]:
            for by in range(-brush, brush + 1):
                for bx in range(-brush, brush + 1):
                    nx, ny = mgx + bx, mgy + by
                    if 0 <= nx < GW and 0 <= ny < GH:
                        box[ny][nx] = ""
            
    # update screen
    scr.fill((0, 0, 0))
    for y, r in enumerate(box):
        for x, t in enumerate(r):
            tdata = ELE.get(t)
            if tdata is not None:
                col = tdata["col"]
                try:
                    if tdata["col"] == "rand": 
                        col = (random.randint(0, 255), 
                               random.randint(0, 255), 
                               random.randint(0, 255))
                    elif isinstance(tdata["col"], str) and tdata["col"].startswith("semirand"):
                        _, r, g, b, r = tdata["col"].split()
                        r, g, b, r = map(int, (r, g, b, r))
                        col = (max(0, min(255, r + random.randint(-r, r))),
                               max(0, min(255, g + random.randint(-r, r))),
                               max(0, min(255, b + random.randint(-r, r))))
                except AttributeError:
                    pass
                pygame.draw.rect(scr, col, pygame.Rect(x * TW, y * TH, TW, TH))
    ptext.draw(f"Selected: {ELE[selTl]["nm"]} ({selTl})\nHovered: {ELE[box[mgy][mgx]]["nm"]} ({box[mgy][mgx]})\n\nSpeed: {spd}\nPaused: {psd}\nBrush Size: {brush * 2 + 1}", (4, 4))
    pygame.display.flip()
    
    # update box
    if not psd:
        nbox = [["" for _ in range(GW)] for _ in range(GH)]
        for y in range(GH - 1, -1, -1):
            for x in range(GW):
                t = box[y][x]
                if not t:
                    continue
                tdata = ELE.get(t)
                if tdata is None:
                    continue
                try:
                    nx, ny = tdata["bhvr"](x, y, tdata.get("arg"))
                except TypeError:
                    continue
                if not nbox[ny][nx]:
                    nbox[ny][nx] = t
                else:
                    nbox[y][x] = t
        box = nbox
    
    # tick speed
    if not psd:
        clk.tick(spd)
    else:
        clk.tick(60)
    
# quit
pygame.quit()
