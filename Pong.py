# Title:- Pong

# Description :-
# In this project, we will build a version of Pong, one of the first arcade video games (1972).
# While Pong is not particularly exciting compared to today's video games, Pong is relatively
# simple to build and provides a nice opportunity to work on the skills that you will need to
# build a game like Asteroids.

import simplegui
import random

# globals variables
WIDTH = 600
HEIGHT = 400
HALF_WIDTH = WIDTH / 2
HALF_HEIGHT = HEIGHT / 2

BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
paddle_pos = []
paddle_vel = []

HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

LEFT = False
RIGHT = True
RESTART = True

def spawn_ball():
    """ Initializes ball_pos and ball_vel for new ball in middle of canvas.
    If direction is RIGHT, the ball's velocity is upper right, else upper left """
    global ball_pos, ball_vel # these are vectors stored as lists
    
    if RESTART:
        ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    if RIGHT:
        ball_vel = [-random.randrange(2, 4), - random.randrange(2, 4)]
    
    else:
        ball_vel = [random.randrange(2, 4), - random.randrange(2, 4)]

# event handlers
def new_game():
    global paddle_pos, paddle_vel, score  
    global RESTART
    
    if RESTART:
        spawn_ball()
        RESTART = False
        
     paddle_pos = [HALF_HEIGHT, HALF_HEIGHT]
     paddle_vel = [0, 0]
     score = [0, 0]

def repeat():
    global RESTART, LEFT, RIGHT
    
    RESTART = True
    RIGHT = True
    LEFT = False
    new_game()

def draw(canvas):
    """ Draw Handler """
    global score, paddle_pos, ball_pos, ball_vel, RIGHT, LEFT, RESTART
    
    frame.set_canvas_background("White")
    
    """ Draws mid line and gutters """
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "Black")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "Black")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1, "Black")
    
    """ Updates paddle's vertical position, keeps paddle on the screen """
    for i in range(2):
        if (paddle_pos[i] >= HALF_PAD_HEIGHT and paddle_pos[i] <= (HEIGHT - HALF_PAD_HEIGHT)):
            paddle_pos[i] -= paddle_vel[i]
    
        elif (paddle_pos[i] <  HALF_PAD_HEIGHT):
            paddle_pos[i] += 1
    
        elif (paddle_pos[i] > (HEIGHT - HALF_PAD_HEIGHT)):
            paddle_pos[i] -= 1
    
    """ Draws the paddles """
    canvas.draw_polygon([[HALF_PAD_WIDTH, paddle_pos[0] - HALF_PAD_HEIGHT], 
                         [HALF_PAD_WIDTH, paddle_pos[0] - HALF_PAD_HEIGHT], 
                         [HALF_PAD_WIDTH, paddle_pos[0] + HALF_PAD_HEIGHT],
                         [HALF_PAD_WIDTH, paddle_pos[0] + HALF_PAD_HEIGHT]], 
                        PAD_WIDTH, 'CC0000')
    
    canvas.draw_polygon([[(WIDTH - HALF_PAD_WIDTH), paddle_pos[1] + HALF_PAD_HEIGHT], 
                         [(WIDTH - HALF_PAD_WIDTH), paddle_pos[1] + HALF_PAD_HEIGHT], 
                         [(WIDTH - HALF_PAD_WIDTH), paddle_pos[1] - HALF_PAD_HEIGHT], 
                         [(WIDTH - HALF_PAD_WIDTH), paddle_pos[1] - HALF_PAD_HEIGHT]], 
                        PAD_WIDTH, 'CC0000')
    
    """ Updates the ball's position"""
    for i in range(2):
        ball_pos[i] += ball_vel[i]
    
    if (ball_pos[1] + BALL_RADIUS) >= HEIGHT:
        ball_vel[1] = -ball_vel[1]
    
    if (ball_pos[1] - BALL_RADIUS) <= 0:
        ball_vel[1] = -ball_vel[1]
    
    if (ball_pos[0] - BALL_RADIUS) <= PAD_WIDTH:
        
        if ((ball_pos[1] <= (paddle_pos[0] + HALF_PAD_HEIGHT + 2)) and
            (ball_pos[1] >= (paddle_pos[0] - HALF_PAD_HEIGHT - 2))):
            
            if ball_vel[0] > 0:
                ball_vel[0] += 1
            
            else:
                ball_vel[0] -= 1
            
            ball_vel[0] = -ball_vel[0]
        
        else:
            RIGHT = False
            LEFT = True
            RESTART = True
            score[1] += 1
            spawn_ball()
    
    if (ball_pos[0] + BALL_RADIUS) >= (WIDTH - PAD_WIDTH):
        
        if ((ball_pos[1] <= (paddle_pos[1] + HALF_PAD_HEIGHT + 2)) and
            (ball_pos[1] >= (paddle_pos[1] - HALF_PAD_HEIGHT - 2))):
            
            if ball_vel[0] > 0:
                ball_vel[0] += 1
            
            else:
                ball_vel[0] -= 1
            
            ball_vel[0] = -ball_vel[0]
        else:
            RIGHT = True
            LEFT = False
            RESTART = True
            score[0] += 1
            spawn_ball()
    
    """ Draws the ball """
    canvas.draw_circle(ball_pos, BALL_RADIUS, 12, "FF6633", "FF6633")
    
    """ Draws the scores """
    for i in range(2):
        canvas.draw_text(str(score[i]),((250 + i*87), 50), 30, "Black")

def keydown(key):
    global paddle_vel
    
    if key == simplegui.KEY_MAP["up"]:
        paddle_vel[1] += 10
    
    elif key == simplegui.KEY_MAP["down"]:
        paddle_vel[1] -= 10
    
    if key == simplegui.KEY_MAP["w"]:
        paddle_vel[0] += 10
    
    elif key == simplegui.KEY_MAP["s"]:
        paddle_vel[0] -= 10

def keyup(key):
    global paddle_vel
    
    if key == simplegui.KEY_MAP["up"]:
        paddle_vel[1] -= 10
    
    elif key == simplegui.KEY_MAP["down"]:
        paddle_vel[1] += 10
    
    if key == simplegui.KEY_MAP["w"]:
        paddle_vel[0] -= 10
    
    elif key == simplegui.KEY_MAP["s"]:
        paddle_vel[0] += 10

# creating the frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', repeat, 60)

# starting the frame
new_game()
frame.start()
