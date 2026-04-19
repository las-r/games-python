from pyray import * #type:ignore
import random

# snake
# made by las-r on github

# settings
WIDTH, HEIGHT = 800, 600
BW, BH = 20, 15
TW, TH = WIDTH // BW, HEIGHT // BH

# helpers
def napple():
    na = [random.randint(0, BW - 1), random.randint(0, BH - 1)]
    while na in snake or na == apple:
        na = [random.randint(0, BW - 1), random.randint(0, BH - 1)]
    return na

def setup():
    global snake, apple, dx, dy, mbuf
    snake = [[BW // 3, BH // 2]]
    apple = [2 * BW // 3, BH // 2]
    dx, dy = 1, 0
    mbuf = False

# window
init_window(WIDTH, HEIGHT, "Snake")
set_target_fps(10)

# setup variables
setup()

# main loop
while not window_should_close():
    # movement input
    if is_key_pressed(KeyboardKey.KEY_W) and (dx, dy) != (0, 1) and not mbuf: 
        dx, dy = 0, -1
        mbuf = True
    if is_key_pressed(KeyboardKey.KEY_S) and (dx, dy) != (0, -1) and not mbuf: 
        dx, dy = 0, 1
        mbuf = True
    if is_key_pressed(KeyboardKey.KEY_A) and (dx, dy) != (1, 0) and not mbuf: 
        dx, dy = -1, 0
        mbuf = True
    if is_key_pressed(KeyboardKey.KEY_D) and (dx, dy) != (-1, 0) and not mbuf: 
        dx, dy = 1, 0
        mbuf = True
    if is_key_pressed(KeyboardKey.KEY_R):
        setup()
    
    # new snake head
    x, y = snake[0]
    x += dx
    y += dy
    nh = [x, y]
    
    # apple check
    if nh == apple:
        apple = napple()
    else:
        snake.pop()
    
    # death check
    if not 0 <= x < BW or not 0 <= y < BH or nh in snake:
        setup()
        continue
        
    # update head
    snake.insert(0, nh)
    mbuf = False
    
    # draw
    begin_drawing()
    clear_background(BLACK)
    for x, y in snake:
        draw_rectangle(x * TW, y * TH, TW, TH, GREEN)
    draw_rectangle(apple[0] * TW, apple[1] * TH, TW, TH, RED)
    end_drawing()

# close
close_window()
