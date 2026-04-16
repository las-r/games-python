import copy
from pyray import * #type:ignore

# conway's game of life
# made by las-r on github
# v1.1

# settings
WIDTH, HEIGHT = 800, 600
BWIDTH, BHEIGHT = 160, 120
TWIDTH, THEIGHT = WIDTH // BWIDTH, HEIGHT // BHEIGHT

# other constants
DIRS = [(0, 1), (0, -1), (1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1)]

# window
init_window(WIDTH, HEIGHT, "Conway's Game of Life")
set_target_fps(60)

# helpers
togrid = lambda p: (int(p.x / TWIDTH), int(p.y / THEIGHT))

# main functions
def countneighbors(board, x, y):
    count = 0
    for d in DIRS:
        try:
            if board[(y + d[1]) % BHEIGHT][(x + d[0]) % BWIDTH]:
                count += 1
        except IndexError:
            pass
    return count

def nextgen(board):
    nboard = copy.deepcopy(board)
    for y in range(BHEIGHT):
        for x in range(BWIDTH):
            n = countneighbors(board, x, y)
            if board[y][x] and (n <= 1 or n >= 4):
                nboard[y][x] = False
            if not board[y][x] and n == 3:
                nboard[y][x] = True
    return nboard

# variables
frames = 0
time = 0
board = [[False for _ in range(BWIDTH)] for _ in range(BHEIGHT)]
text = True
fpg = 6
paused = True
grid = True
pop = 0

# main loop
while not window_should_close():
    frames += 1
    
    # key input
    if is_key_pressed(KeyboardKey.KEY_R):
        board = [[False for _ in range(BWIDTH)] for _ in range(BHEIGHT)]
        time = 0
    if is_key_pressed(KeyboardKey.KEY_T):
        text = not text
    if is_key_pressed(KeyboardKey.KEY_G):
        grid = not grid
    if is_key_pressed(KeyboardKey.KEY_SPACE):
        paused = not paused
        
    # fps input
    fpg = max(1, fpg + int(get_mouse_wheel_move()))
    
    # board input
    mx, my = togrid(get_mouse_position())
    if 0 <= mx < BWIDTH and 0 <= my < BHEIGHT:
        if is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT):
            board[my][mx] = True
        if is_mouse_button_down(MouseButton.MOUSE_BUTTON_MIDDLE):
            board[my][mx] = not board[my][mx]
        if is_mouse_button_down(MouseButton.MOUSE_BUTTON_RIGHT):
            board[my][mx] = False
            
    # next generation
    if not paused:
        if not frames % fpg:
            board = nextgen(board)
            time += 1
        
    # draw board
    begin_drawing()
    clear_background(BLACK)
    pop = 0
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                draw_rectangle(x * TWIDTH, y * THEIGHT, TWIDTH, THEIGHT, WHITE)
                pop += 1
                
    # draw grid
    if grid:
        for x in range(BWIDTH):
            draw_line(x * TWIDTH, 0, x * TWIDTH, HEIGHT, Color(20, 20, 20, 255))
        for y in range(BHEIGHT):
            draw_line(0, y * THEIGHT, WIDTH, y * THEIGHT, Color(20, 20, 20, 255))
            
    # draw hover outline
    draw_rectangle_lines(mx * TWIDTH, my * THEIGHT, TWIDTH, THEIGHT, PURPLE)
                
    # text
    if text:
        draw_text(f"Paused: {paused}", 5, 5, 20, PURPLE)
        draw_text(f"Frames per generation: {fpg}", 5, 30, 20, PURPLE)
        draw_text(f"Hovered: {mx, my}", 5, 55, 20, PURPLE)
        draw_text(f"Time: {time}", 5, 80, 20, PURPLE)
        draw_text(f"Population: {pop}", 5, 105, 20, PURPLE)
    end_drawing()

# close
close_window()
