# Title :- Stopwatch: The Game

# Description :- 
# Our mini-project for this week will focus on combining text drawing in the canvas with timers
# to build a simple digital stopwatch that keeps track of the time in tenths of a second. The
# stopwatch should contain "Start", "Stop" and "Reset" buttons. 

import simplegui
import time

# global variables
current = "0:00.0"
score = "0/0"
iterable = 0
corr_guess = 0
tot_guess = 0
alStop = True

# helper function format that converts time in tenths of seconds into formatted string A:BC.D
def format(tmp):
    global current
    
    msec = tmp % 10
    sec = tmp / 10
    
    if sec >= 60:
        mnu = sec / 60
        sec = sec % 60
    
    else:
        mnu = 0
    
    if len(str(sec)) == 1:
        cor_sec = '0' + str(sec)
    
    else:
        cor_sec = str(sec)
    
    current = str(mnu) + ':' + cor_sec + '.' + str(msec)    

# event handlers for buttons
def start_handler():
    """ Event handler for button - Start """
    global alStop
    
    alStop = False
    timer.start()

def stop_handler():
    """ Event handler for button - Stop """
    global tot_guess, corr_guess, score, alStop
    
    timer.stop()
    if not alStop:
        alStop = True
        tot_guess += 1
        
        if current.endswith('.0'):
            corr_guess += 1
        
        score = str(corr_guess) + '/' + str(tot_guess)
        

def reset_handler():
    """ Event handler for button - Restart """
    global tot_guess, corr_guess, score, iterable
    
    timer.stop()
    iterable = 0
    format(iterable)
    tot_guess = corr_guess = 0
    score = '0/0'

# event handler for timer with 0.1 sec interval
def timer_handler():
    """ Event handler for timer with 0.1 sec interval """
    global iterable
    
    iterable += 1
    format(iterable)

# draw handler
def draw_handler(canvas):
    
    canvas.draw_text(current, (90, 110), 40, 'White')
    canvas.draw_text(score, (210, 30), 40, 'Green')
    
# creating the frame
frame = simplegui.create_frame('Stop Watch', 300, 200)
timer = simplegui.create_timer(100, timer_handler)

# registering the event handlers
frame.add_button('Start', start_handler, 100)
frame.add_button('Stop', stop_handler, 100)
frame.add_button('Reset', reset_handler, 100)
frame.set_draw_handler(draw_handler)

# starting the frame
frame.start()
