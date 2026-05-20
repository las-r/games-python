from pyray import * #type:ignore
import random
import math

# gravity simulation
# made by las-r

# settings
WIDTH, HEIGHT = 800, 600
GRAVSCALE = 1

# body
class Body:
    def __init__(self, pos, mass, vel, col):
        self.pos = pos
        self.mass = mass
        self.vel = vel
        self.col = col
        
# visual size helper
def visrad(mass):
    logm = math.log10(mass) if mass > 1 else 2.0
    rad = int(4 + 4.84 * (logm - 2.0))
    if rad < 4:
        rad = 4
    return rad

# init
init_window(WIDTH, HEIGHT, "Gravity Simulation")
set_target_fps(60)

# bodies
bodies = []

# main loop
paused = False
spawning = False
while not window_should_close():
    dt = get_frame_time()
    
    # input
    if is_key_pressed(KeyboardKey.KEY_R):
        bodies = []
    if is_key_pressed(KeyboardKey.KEY_SPACE):
        paused = not paused
    
    # spawning
    if is_mouse_button_pressed(0):
        if not spawning:
            spawning = True
            spos = get_mouse_position()
            smass = 100
            scol = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
        else:
            nb = Body(spos, smass, svel, scol)
            bodies.append(nb)
            spawning = False
    if spawning:
        wheel = get_mouse_wheel_move()
        if wheel > 0:
            smass *= 1.25
        elif wheel < 0:
            smass /= 1.25
        svel = vector2_subtract(get_mouse_position(), spos)
    
    # update
    if not paused and not spawning:
        for b in bodies:
            ta = Vector2(0, 0)
            for d in bodies:
                if b == d: 
                    continue
                f = (d.mass * GRAVSCALE) / (vector2_distance_sqr(b.pos, d.pos) + 10)
                nd = vector2_normalize(vector2_subtract(d.pos, b.pos))
                a = vector2_scale(nd, f)
                ta = vector2_add(ta, a)
            b.vel = vector2_add(b.vel, vector2_scale(ta, dt))
            b.pos = vector2_add(b.pos, vector2_scale(b.vel, dt))
    
    # draw
    begin_drawing()
    clear_background(BLACK)
    for b in bodies:
        draw_circle(int(b.pos.x), int(b.pos.y), visrad(b.mass), b.col)
    if spawning:
        m = get_mouse_position()
        draw_circle(int(spos.x), int(spos.y), visrad(smass), scol)
        draw_line(int(spos.x), int(spos.y), int(m.x), int(m.y), scol)
        draw_text(f"svx: {round(svel.x, 2)}", 250, 10, 24, WHITE)
        draw_text(f"svy: {round(svel.y, 2)}", 250, 35, 24, WHITE)
        draw_text(f"smass: {smass}", 250, 60, 24, WHITE)
    end_drawing()
    

# deinit
close_window()
