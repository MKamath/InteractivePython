# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
HALF_WIDTH = WIDTH / 2
HALF_HEIGHT = HEIGHT / 2
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
RESTART = True

def spawn_ball():
    """ 
    Initializes ball_pos and ball_vel for new ball in middle of canvas.
    If direction is RIGHT, the ball's velocity is upper right, else upper left
    """
    global ball_pos, ball_vel # these are vectors stored as lists
    if RESTART:
        ball_pos = [WIDTH / 2, HEIGHT / 2]
    if RIGHT:
        ball_vel = [-random.randrange(2, 4), - random.randrange(2, 4)]
    else:
        ball_vel = [random.randrange(2, 4), - random.randrange(2, 4)]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel # these are numbers
    global score1, score2  # these are ints
    global RESTART
    if RESTART:
        spawn_ball()
        RESTART = False
    paddle1_pos = HALF_HEIGHT
    paddle2_pos = HALF_HEIGHT
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0

def repeat():
    global RESTART, LEFT, RIGHT
    RESTART = True
    RIGHT = True
    LEFT = False
    new_game()

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global RIGHT, LEFT, RESTART
    frame.set_canvas_background("White")
    
    """ Draws mid line and gutters """
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "Black")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "Black")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],
                     [WIDTH - PAD_WIDTH, HEIGHT], 1, "Black")
    
    """ Updates paddle's vertical position, 
        keeps paddle on the screen """
    if (paddle1_pos >= HALF_PAD_HEIGHT and 
        paddle1_pos <= (HEIGHT - HALF_PAD_HEIGHT)):
        paddle1_pos -= paddle1_vel
    elif (paddle1_pos <  HALF_PAD_HEIGHT):
        paddle1_pos += 1
    elif (paddle1_pos > (HEIGHT - HALF_PAD_HEIGHT)):
        paddle1_pos -= 1
    
    if (paddle2_pos >= HALF_PAD_HEIGHT and 
        paddle2_pos <= (HEIGHT - HALF_PAD_HEIGHT)):
        paddle2_pos -= paddle2_vel
    elif (paddle2_pos < HALF_PAD_HEIGHT):
        paddle2_pos += 1
    elif (paddle2_pos > (HEIGHT - HALF_PAD_HEIGHT)):
        paddle2_pos -= 1
    
    """ Draws the paddles """
    canvas.draw_polygon([[HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], 
                         [HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], 
                         [HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT],
                         [HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT]], 
                        PAD_WIDTH, 'CC0000')
    canvas.draw_polygon([[(WIDTH - HALF_PAD_WIDTH), paddle2_pos + HALF_PAD_HEIGHT], 
                         [(WIDTH - HALF_PAD_WIDTH), paddle2_pos + HALF_PAD_HEIGHT], 
                         [(WIDTH - HALF_PAD_WIDTH), paddle2_pos - HALF_PAD_HEIGHT], 
                         [(WIDTH - HALF_PAD_WIDTH), paddle2_pos - HALF_PAD_HEIGHT]], 
                        PAD_WIDTH, 'CC0000')
    
    """ Updates the ball's position"""
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    if (ball_pos[1] + BALL_RADIUS) >= HEIGHT:
        ball_vel[1] = -ball_vel[1]
    
    if (ball_pos[1] - BALL_RADIUS) <= 0:
        ball_vel[1] = -ball_vel[1]
    
    if (ball_pos[0] - BALL_RADIUS) <= PAD_WIDTH:
        if ((ball_pos[1] <= (paddle1_pos + HALF_PAD_HEIGHT + 2)) and
            (ball_pos[1] >= (paddle1_pos - HALF_PAD_HEIGHT - 2))):
            if ball_vel[0] > 0:
                ball_vel[0] += 1
            else:
                ball_vel[0] -= 1
            ball_vel[0] = -ball_vel[0]
        else:
            RIGHT = False
            LEFT = True
            RESTART = True
            score2 += 1
            spawn_ball()
    
    if (ball_pos[0] + BALL_RADIUS) >= (WIDTH - PAD_WIDTH):
        if ((ball_pos[1] <= (paddle2_pos + HALF_PAD_HEIGHT + 2)) and
            (ball_pos[1] >= (paddle2_pos - HALF_PAD_HEIGHT - 2))):
            if ball_vel[0] > 0:
                ball_vel[0] += 1
            else:
                ball_vel[0] -= 1
            ball_vel[0] = -ball_vel[0]
        else:
            RIGHT = True
            LEFT = False
            RESTART = True
            score1 += 1
            spawn_ball()
    
    """ Draws the ball """
    canvas.draw_circle(ball_pos, BALL_RADIUS, 12, "FF6633", "FF6633")
    
    """ Draws the scores """
    canvas.draw_text(str(score1),(250, 50), 30, "Black")
    canvas.draw_text(str(score2),(337, 50), 30, "Black")

def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel += 10
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel -= 10
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel += 10
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel -= 10

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= 10
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += 10
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= 10
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += 10

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', repeat, 60)

# start frame
new_game()
frame.start()
