#!/usr/bin/env python
#IFS machine...
#

#TODO:
#Abstract interface, to allow for a pygame, a PIL, or GTK canvas whatever
#Handle colors nicely
#Add options
#Pythonify it!!!
#Seperate, but add a transform editor.
#Options are:
#width, height, iterations, skiplen, how to plot (PIL, pygame, GTK, both?)
#scale, x and y offsets, 
#add autoscaling

import sys

#To be honest, we don't really need numpy for this...
try:
    import numpy as np
    random_float = np.random.ranf
except ImportError:
    print "numpy not available, using random instead."
    import random
    random_float = random.random
        
    

#Constants used to index tuples
RULE_A_I = 0
RULE_B_I = 1
RULE_C_I = 2
RULE_D_I = 3
RULE_E_I = 4
RULE_F_I = 5

PROB_I = 0
RULE_I = 1


def load_transform(string, sep = ','):
    """Load a string description of a matrix."""
    a,b,c,d,e,f = [float(i.strip()) for i in string.split(sep)]
    prob = abs(a*d-b*c)
    if prob < .01: prob = .01
    return (prob, (a,b,c,d,e,f))

def load_file(file):
    fd = open(file)
    lines = fd.readlines()
    if lines[-1] == '\n': lines = lines[:-1]
    transforms = [load_transform(t.strip()) for t in lines]
    s = sum([i[0] for i in transforms])
    return [(i[0]/s, i[1]) for i in transforms]

def transform_point(point, transform):
    return transform * point


def calculate_transform(x, y, rule):
    """x, y are the current x and y values, and rule is
a tuple containing the (a,b,c,d,e,f) values.
Return a (x,y) tuple"""
    a,b,c,d,e,f = rule
    t = a*x+b*y+e
    y = c*x+d*y+f
    return (t, y)

def choose_rule(probs):
    """Return the index of the rule chosen."""
    chosen = 0
    lim = random_float()
    prob = probs[chosen]
    while prob < lim:
        chosen += 1
        prob += probs[chosen]
    return chosen

def run_IFS(iters, skip, rules, draw_method, speak_method = None,\
            announce_interval = None, xy = None):
    """Run the IFS iteration loop
    
iters: number of iterations
skip: number of iterations to skip (the first 100 or so won't be accurate)
rules: a list of rules and their probabilities. Looks like: [(probs, rule)...
draw_method: a function to be called each iteration after skip. This function
    must take x and y as arguments, and also chosen (If you're colorising).
    This could be a method to draw to a GUI canvas, or to draw to an image file,
    or even something that simply uses the x and y values to calculate how
    big a canvas would need to be.
    Note, that the x and y values will be in their raw decimal form, so
    any scaling must be performed by your function
speak_method: a function to be called to announce the progress. It will be
    called with speak_method(x, y, current iteration).
announce_interval: This will be used to calculate when we need to
    call speak_method. Every announce_interval iterations, speak_method will
    be called. eg. if you had 100000 iterations, you might want to set
    announce_interval to 1000
xy: a tuple with x,y coordinates. You might want to use this to pick up a
    calculation where it left off, for example."""
    
    probs = [r[PROB_I] for r in rules]
    rules = [r[RULE_I] for r in rules]
    
    i = 0

    if xy:
        x,y = xy
    else:
        x = random_float()
        y = random_float()

    while i < iters + skip:
        chosen = choose_rule(probs)
        x, y = calculate_transform(x, y, rules[chosen])
        
        if i > skip:
            draw_method(x, y, chosen)
        #Announce the results
        if not speak_method: pass
        elif i%announce_interval == 0:
            speak_method(x, y, i)

        i += 1


def calculate_best_settings(rules, scale, iters = 10000, skip = 100):
    """Return a tuple of width and height and x_off and y_off settings
((w,h),(x_off, y_off))"""
    #note, I know this is ugly, I don't know how else to do it though
    global GLOBAL_h_x, GLOBAL_h_y, GLOBAL_l_x, GLOBAL_l_y
    GLOBAL_h_x = GLOBAL_h_y = GLOBAL_l_x = GLOBAL_l_y = 0

    def draw_method(x, y, chosen):
        global GLOBAL_h_x, GLOBAL_h_y, GLOBAL_l_x, GLOBAL_l_y
        if x*scale > GLOBAL_h_x: GLOBAL_h_x = x*scale
        elif x*scale < GLOBAL_l_x: GLOBAL_l_x = x*scale
        if y*scale > GLOBAL_h_y: GLOBAL_h_y = y*scale
        elif y*scale < GLOBAL_l_y: GLOBAL_l_y = y*scale
        
    run_IFS(iters, skip, rules, draw_method)
    hx,lx,hy,ly = GLOBAL_h_x, GLOBAL_l_x, GLOBAL_h_y, GLOBAL_l_y
    width = abs(lx)+abs(hx)
    height = abs(ly)+abs(hy)
    x_off = abs(lx)
    y_off = abs(ly)

    return ((width, height), (x_off, y_off))

if __name__ == "__main__":
    rules = load_file(sys.argv[1])
    scale = int(sys.argv[2])
    try: its = int(sys.argv[3])
    except IndexError: its = 100000
    skip = 1000
    dim, offsets = calculate_best_settings(rules, scale)
    x_off, y_off = offsets
    import Image as im
    import pygame
    
    screen = pygame.display.set_mode(dim)
    
    
    color = ((255,0,0),(0,255,0),(0,0,255),(255,255,255), (255, 255,0), (0, 255, 255), (255, 0,255))

    #pix = screen.load()
    
    def draw_method(x, y, chosen):
        screen.set_at((int(x*scale)+x_off, int(y*scale)+y_off),color[chosen])

    def speak_method(x, y, i):
        pygame.display.flip()
        
    run_IFS(its, skip, rules, draw_method, speak_method, 1000)
        
    print "Done!"
    raw_input()
