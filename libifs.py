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
    return [prob, [a,b,c,d,e,f]]

def load_str(string):
    lines = [s.strip() for s in string.split("\n")]
    lines = [s for s in lines if s]

    transforms = [load_transform(t.strip()) for t in lines]
    s = sum([i[0] for i in transforms])
    return [[i[0]/s, i[1]] for i in transforms]
    
def load_file(file):
    fd = open(file)
    tr = load_str(fd.read())
    fd.close()
    return tr
    


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

def generate_IFS(iters, skip, rules):
    """Run the IFS iteration loop, yielding a tuple of
(x_coord, y_coord, index_of_chosen_rule, iterations_passed)
    
iters: number of iterations
skip: number of iterations to skip (the first 100 or so won't be accurate)
rules: a list of rules and their probabilities. Looks like: [(probs, rule)]

NOTE: The _most_ important thing to remember about this is that all coordinates
returned are in the cartesian plane, where the axes grow in all directions,
whereas in most computer coordinate systems the y-axis grows downwards.
So make sure you account for this. One easy way to convert cartesian to
graphics coordinates is (height_of_drawing_area - y_coordinate)."""
    
    probs = [r[PROB_I] for r in rules]
    rules = [r[RULE_I] for r in rules]
    
    x = random_float()
    y = random_float()

    i = 0
    
    while i < iters + skip:
        chosen = choose_rule(probs)
        x, y = calculate_transform(x, y, rules[chosen])
        
        if i > skip:
            yield (x, y, chosen, i)
        i += 1


def calculate_best_settings(rules, scale, iters = 20000, skip = 100):
    """Return a tuple of width and height and x_off and y_off settings
((w,h),(x_off, y_off))"""
    h_x = l_x = h_y = l_y = 0
    
    for x, y, _, _ in generate_IFS(iters, skip, rules):
        if x > h_x: h_x = x
        if x < l_x: l_x = x
        if y > h_y: h_y = y
        if y < l_y: l_y = y

    width = int((abs(l_x)+abs(h_x)) * scale)
    height = int((abs(l_y)+abs(h_y)) * scale)
    x_off = int(abs(l_x) * scale)
    y_off = int(abs(l_y) * scale)
    
    return ((width, height), (x_off, y_off))

