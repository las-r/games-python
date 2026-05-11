from pyray import * #type:ignore
import math #type:ignore

# 3d graphing calculator
# made by las-r on github

# window
init_window(1000, 700, "3D Graphing Calculator")
set_target_fps(60)
disable_cursor()

# function to rebuild lines
def rebuildl():
    global lcache
    lcache.clear()
    x = -size
    while x < size:
        y = -size
        while y < size:
            try:
                z1 = f(x, y)
                z2 = f(x + step, y)
                z3 = f(x, y + step)
                p1 = Vector3(x, z1, y)
                p2 = Vector3(x + step, z2, y)
                p3 = Vector3(x, z3, y + step)
                lcache.append((p1, p2))
                lcache.append((p1, p3))
            except Exception:
                pass
            y += step
        x += step

# function to graph
func = "math.sin(x) + math.cos(y)"
def f(x, y):
    return eval(func, {"math": math}, {"x": x, "y": y})

# camera
cam = Camera3D()
cam.position = Vector3(8, 8, 8)
cam.target = Vector3(0, 0, 0)
cam.up = Vector3(0, 1, 0)
cam.fovy = 45
cam.projection = CameraProjection.CAMERA_PERSPECTIVE

# graph settings
step = 0.25
size = 5

# graph cache and initial build
lcache = []
rebuildl()

# text input state
typing = False
inpbuf = func

# main loop
while not window_should_close():
    # cam movement
    update_camera(cam, CameraMode.CAMERA_ORBITAL)
    
    # old values
    osize = size
    ostep = step
    ofunc = func
        
    # typing
    if typing:
        # get character
        key = get_char_pressed()
        while key > 0:
            if 32 <= key <= 125:
                inpbuf += chr(key)
            key = get_char_pressed()
        
        # backspace and enter
        if is_key_pressed(KeyboardKey.KEY_BACKSPACE):
            inpbuf = inpbuf[:-1]
        if is_key_pressed(KeyboardKey.KEY_ENTER):
            func = inpbuf
            typing = False
    else:
        if is_key_down(KeyboardKey.KEY_PERIOD): size += 0.05
        if is_key_down(KeyboardKey.KEY_COMMA): size = max(1, size - 0.05)
        if is_key_pressed(KeyboardKey.KEY_EQUAL):  step += 0.25
        if is_key_pressed(KeyboardKey.KEY_MINUS): step = max(0.25, step - 0.25)
        if is_key_pressed(KeyboardKey.KEY_R): 
            step = 1
            size = 5
        if is_key_pressed(KeyboardKey.KEY_F):
            typing = not typing
            if typing:
                inpbuf = func
        
    # check for rebuild
    if size != osize or step != ostep or func != ofunc:
        rebuildl()

    # draw begin
    begin_drawing()
    clear_background(BLACK)
    begin_mode_3d(cam)
    draw_grid(100, 1)

    # draw cached lines
    for line in lcache:
        draw_line_3d(line[0], line[1], GREEN)

    # draw end
    end_mode_3d()
    if typing:
        draw_rectangle(10, 650, 980, 40, DARKGRAY)
        draw_text("f(x,y) = " + inpbuf, 20, 660, 20, GREEN)
    draw_text(f"step: {step}", 10, 10, 20, WHITE)
    draw_text(f"size: {size:.2f}", 10, 35, 20, WHITE)
    draw_text(f"function: {func}", 10, 60, 20, WHITE)
    end_drawing()

close_window()
