from pyray import * #type:ignore
from numba import njit

# mandelbrot set explorer
# made by las-r on github

# settings
WIDTH, HEIGHT = 800, 450
BOUND = 2
MAXITER = 50

# mandelbrot function
@njit
def ziter(cr, ci):
    x, y = 0.0, 0.0
    for i in range(MAXITER):
        x2, y2 = x*x, y*y
        if x2 + y2 > 4: return i
        y = 2*x*y + ci
        x = x2 - y2 + cr
    return MAXITER

# helpers
def creal(px):
    vw = 3.0 / zoom 
    return tx + (px / sw - 0.5) * vw
def cimag(py):
    vh = (3.0 / zoom) / asp
    return ty + (py / sh - 0.5) * vh

# window
init_window(WIDTH, HEIGHT, "Mandelbrot Set")
set_target_fps(60)

# setup colors
colors = []
for i in range(MAXITER):
    colors.append(color_from_hsv(i * 10 % 360, 0.8, 1.0))
colors.append(BLACK)

# variables
tx, ty = -0.5, 0.0
zoom = 1.0
scale = 10

# other variables
sw, sh = WIDTH // scale, HEIGHT // scale
asp = sw / sh

# setup image
img = gen_image_color(sw, sh, BLACK)
tex = load_texture_from_image(img)

# main loop
while not window_should_close():
    # movement
    mspd = 0.1 / zoom
    if is_key_down(KeyboardKey.KEY_W) or is_key_down(KeyboardKey.KEY_UP): ty -= mspd
    if is_key_down(KeyboardKey.KEY_S) or is_key_down(KeyboardKey.KEY_DOWN): ty += mspd
    if is_key_down(KeyboardKey.KEY_A) or is_key_down(KeyboardKey.KEY_LEFT): tx -= mspd
    if is_key_down(KeyboardKey.KEY_D) or is_key_down(KeyboardKey.KEY_RIGHT): tx += mspd
    
    # zoom
    if is_key_down(KeyboardKey.KEY_Q): zoom /= 1.1
    if is_key_down(KeyboardKey.KEY_E): zoom *= 1.1
    
    # scale
    if is_key_pressed(KeyboardKey.KEY_MINUS): scale -= 1
    if is_key_pressed(KeyboardKey.KEY_EQUAL): scale += 1
    
    # reset
    if is_key_pressed(KeyboardKey.KEY_R):
        tx, ty = -0.5, 0.0
        zoom = 1.0
    
    # fix scale
    if is_key_pressed(KeyboardKey.KEY_MINUS) or is_key_pressed(KeyboardKey.KEY_EQUAL):
        scale = max(1, scale)
        sw, sh = WIDTH // scale, HEIGHT // scale
        asp = sw / sh
        unload_image(img)
        unload_texture(tex)
        img = gen_image_color(sw, sh, BLACK)
        tex = load_texture_from_image(img)
    
    # create image
    for py in range(sh):
        for px in range(sw):
            i = ziter(creal(px), cimag(py))
            image_draw_pixel(img, px, py, colors[i])
    update_texture(tex, img.data)
    
    # draw mandelbrot image
    begin_drawing()
    clear_background(BLACK)
    draw_texture_ex(tex, (0,0), 0, scale, WHITE)
    
    # draw text
    draw_text(f"FPS: {get_fps()}", 5, 5, 20, WHITE)
    draw_text(f"Tar. X: {tx}", 5, 30, 20, WHITE)
    draw_text(f"Tar. Y: {ty}", 5, 55, 20, WHITE)
    draw_text(f"Zoom: {zoom}", 5, 80, 20, WHITE)
    draw_text(f"Ren. Upscale: {scale}", 5, 105, 20, WHITE)
    end_drawing()

# close
close_window()
