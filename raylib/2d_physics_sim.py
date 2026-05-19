from pyray import * #type:ignore
import random

# 2d physics sim
# by las-r

# point
class Point:
    def __init__(self, pos: Vector2, vel: Vector2, e, r, col):
        self.pos = pos
        self.vel = vel
        self.e = e
        self.r = r
        self.col = col

# init
WIDTH, HEIGHT = 800, 600
init_window(WIDTH, HEIGHT, "2D Physics Simulation")
set_target_fps(60)

# settings
grav = Vector2(0, 500)

# point list
points = []

# main loop
paused = False
while not window_should_close():
    dt = get_frame_time()
    
    # input
    if is_mouse_button_down(0):
        m = get_mouse_position()
        points.append(
            Point(
                Vector2(m.x, m.y),
                Vector2(random.randint(-200, 200), 0),
                random.uniform(0.2, 0.8),
                random.randint(10, 20),
                Color(
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                    255
                )
            )
        )
    
    if is_key_pressed(KeyboardKey.KEY_R):
        points = []
    if is_key_pressed(KeyboardKey.KEY_SPACE):
        paused = not paused
    
    if not paused:
        for i, p in enumerate(points):
            # update pos
            p.pos = vector2_add(p.pos, vector2_scale(p.vel, dt))
            
            # update vel
            p.vel = vector2_add(p.vel, vector2_scale(grav, dt))
            
            # point bounce
            for q in [q for q in points if q != p]:
                d = vector2_distance(p.pos, q.pos)
                sr = p.r + q.r
                if d < sr:
                    # separate
                    n = vector2_normalize(vector2_subtract(q.pos, p.pos))
                    o = (sr - d) / 2
                    m_vec = vector2_scale(n, o)
                    p.pos = vector2_subtract(p.pos, m_vec)
                    q.pos = vector2_add(q.pos, m_vec)
                    nv = vector2_dot_product(vector2_subtract(q.vel, p.vel), n)
                    if 0 > nv:
                        # impulse
                        e = min(p.e, q.e)
                        j = -(1 + e) * nv / 2
                        impulse = vector2_scale(n, j)
                        p.vel = vector2_subtract(p.vel, impulse)
                        q.vel = vector2_add(q.vel, impulse)
            
            # wall bounce
            if p.pos.x - p.r < 0:
                p.pos.x = p.r
                p.vel.x *= -p.e
                p.vel.x = abs(p.vel.x)
            if p.pos.x + p.r > WIDTH:
                p.pos.x = WIDTH - p.r
                p.vel.x *= -p.e
                p.vel.x = -abs(p.vel.x)
            if p.pos.y - p.r < 0:
                p.pos.y = p.r
                p.vel.y *= -p.e
                p.vel.y = abs(p.vel.y)
            if p.pos.y + p.r > HEIGHT:
                p.pos.y = HEIGHT - p.r
                p.vel.y *= -p.e
                p.vel.y = -abs(p.vel.y)
    
    # draw points
    begin_drawing()
    clear_background(BLACK)
    for p in points:
        draw_circle_v(p.pos, p.r, p.col)
    end_drawing()

# deinit
close_window()
