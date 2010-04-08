#!/usr/bin/env python
#
#       libifs.py
#       
#       Copyright 2010 Emmanuel Jacyna <xavieran.lives@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.



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
    fd.close()
    if lines[-1] == '\n': lines = lines[:-1]
    transforms = [load_transform(t.strip()) for t in lines]
    s = sum([i[0] for i in transforms])
    return [(i[0]/s, i[1]) for i in transforms]


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

def run_IFS(iters, skip, rules, draw_method, speak_method=None,\
            announce_interval=None, xy=None, i=0):
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
    width = int(abs(lx)+abs(hx))
    height = int(abs(ly)+abs(hy))
    x_off = int(abs(lx))
    y_off = int(abs(ly))

    return ((width, height), (x_off, y_off))
