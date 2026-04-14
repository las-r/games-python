from pyray import * #type:ignore
import random

# pong
# made by las-r on github

# settings
WIDTH, HEIGHT = 800, 400
PSPD = 10
PW = 10
PH = 60
BRAD = 5
BDIRS = (12, -12)

# init window
init_window(WIDTH, HEIGHT, "Pong")
set_target_fps(60)

# variables
p1 = HEIGHT // 2
p2 = HEIGHT // 2
bx, by = WIDTH // 2, HEIGHT // 2
bdx, bdy = random.choice(BDIRS), random.choice(BDIRS)

# main loop
while not window_should_close():
    # input
    if is_key_down(KeyboardKey.KEY_W):
        p1 -= PSPD
    if is_key_down(KeyboardKey.KEY_S):
        p1 += PSPD
    if is_key_down(KeyboardKey.KEY_UP):
        p2 -= PSPD
    if is_key_down(KeyboardKey.KEY_DOWN):
        p2 += PSPD
    p1 = max(0, min(p1, HEIGHT - PH))
    p2 = max(0, min(p2, HEIGHT - PH))
    
    # ball
    bx += bdx
    by += bdy
    if by - BRAD <= 0 or by + BRAD >= HEIGHT:
        bdy *= -1
        by = max(BRAD, min(by, HEIGHT - BRAD))
    if bx - BRAD <= 50 + PW and bx > 50:
        if p1 <= by <= p1 + PH:
            bdx = abs(bdx)
            bx = 50 + PW + BRAD
            
    # paddle-ball bounce
    if bx + BRAD >= (WIDTH - 50) and bx < (WIDTH - 50 + PW):
        if p2 <= by <= p2 + PH:
            bdx = -abs(bdx)
            bx = (WIDTH - 50) - BRAD
    if bx < 0 or bx > WIDTH:
        bx, by = WIDTH // 2, HEIGHT // 2
        bdx = random.choice(BDIRS)
        bdy = random.choice(BDIRS)
        
        
    # draw
    begin_drawing()
    clear_background(BLACK)
    
    # centerline
    draw_line(WIDTH // 2, 0, WIDTH // 2, HEIGHT, GRAY)
    
    # paddles
    draw_rectangle(50, p1, PW, PH, WHITE)
    draw_rectangle(WIDTH - 50, p2, PW, PH, WHITE)
    
    # ball
    draw_circle(bx, by, BRAD, WHITE)
    
    end_drawing()
        
# close
close_window()
