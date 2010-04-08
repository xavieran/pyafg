#!/usr/bin/env python
#IFS machine...
#

#TODO:
#Handle colors nicely
#Add options
#Seperate, but add a transform editor.
#Options are:
#width, height, iterations, skiplen, how to plot (PIL, pygame, GTK, both?)
#scale, x and y offsets, 

import sys

#To be honest, we don't really need numpy for this...
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


global VERBOSITY
VERBOSITY = 1

V_SHOWSTOPPER = 0
V_ESSENTIAL = 1
V_NORMAL = 2
V_DEBUG = 3

COLOR_NORMAL = 0
COLOR_REGION = 1
COLOR_FANCY = 2 #Y'know, it's the, uh, one that makes the image look... gradual?


def message(msg, importance, fd = None):
    if importance <= VERBOSITY:
        if fd:
            fd.write(msg)
        else:
            print msg

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
    width = abs(lx)+abs(hx)
    height = abs(ly)+abs(hy)
    x_off = abs(lx)
    y_off = abs(ly)

    return ((width, height), (x_off, y_off))


def verify_string(string, regex):pass

def split_int(s, inter):
    return [s[x:x+inter] for x in xrange(0, len(s), inter)]

def string2color(s):
    return [int(i) for i in split_int(s, 3)]

def load_colors_from_file(file):
    fd = open(file)
    lines = fd.readlines()
    fd.close()
    return [string2color(x.strip()) for x in lines if not x[0] == '#']

if __name__ == "__main__":
    #width, height, iterations, skiplen, how to plot (PIL, pygame, GTK, both?)
#scale, x and y offsets,
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-s", "--scale", type = "int", default = 0)
    parser.add_option("-x", "--x-offset", type = "int", default = 0)
    parser.add_option("-y", "--y-offset", type = "int", default = 0)
    parser.add_option("-g", "--geometry", type = "string", default = "")
    parser.add_option("-i", "--iterations", type = "int", default = 100000)
    parser.add_option("--color-type", type = "int", default = COLOR_NORMAL)
    parser.add_option("--color", type = "string", default = "000255000")
    parser.add_option("--color-file", type = "string", default = "")
    parser.add_option("-o", "--save", type = "string", default = "")
    parser.add_option("-q", "--quiet", action = "store_false",\
                      default = "verbosity")
    parser.add_option("--progress", action = "store_true", default = False)
    parser.add_option("-v", "--verbosity", action = "store", type = "int",\
                      default = 1)
    opts, args = parser.parse_args(sys.argv)
    args = args[1:]
    #Begin parsing arguments
#    global VERBOSITY
    VERBOSITY = opts.verbosity
    message("Beginning option parsing", V_DEBUG)
    scale = opts.scale
    if not scale:
        parser.error("argument -s/--scale is compulsory!")
        
    rules = load_file(args[0])
    
    its = opts.iterations

    if opts.color_file: colors = load_colors_from_file(opts.color_file)
    else: colors = []
    
    if opts.color_type == COLOR_NORMAL:
        if opts.color_file: color = colors[0]
        else: color = string2color(opts.color)

    elif opts.color_type == COLOR_REGION:
        if opts.color_file: color = colors
        elif len(opts.color) > 9:
            #
            color = [string2color(x) for x in split_int(opts.color, 9)]
            #((0,255,0),(0,255,0),(0,0,255),(255,255,255), (255, 255,0), (0, 255, 255), (255, 0,255))

    elif opts.color_type == COLOR_FANCY:
        color = int(opts.color[0])
        
    skip = 500

    if not (opts.geometry and opts.x_offset and opts.y_offset):
        dim, offsets = calculate_best_settings(rules, scale)
        
    if opts.geometry: dim = [int(i) for i in opts.geometry.split("x")]
    else: dim = int(dim[0]), int(dim[1])
    if opts.x_offset: x_off = opts.x_offset
    else: x_off = int(offsets[0])
    if opts.y_offset: y_off = opts.y_offset
    else: y_off = int(offsets[1])
    
    if opts.save:
        import Image as im
        image = True
        screen = im.new("RGB", dim)
        pix = screen.load()
    else:
        import pygame
        image = False
        screen = pygame.display.set_mode(dim)
    
    message("Finished option parsing", V_DEBUG)
    

    def pixel_set(xy, color):
        color = tuple(color)
        if image:
            try: pix[xy[0],xy[1]] = color#(color[0],color[1],color[2],255)
            except IndexError:pass
        else:
            screen.set_at(xy, color)

    global pixel_count
    pixel_count = {}
    
    def normal(x, y, chosen):
        pixel_set((int(x*scale)+x_off, int(y*scale)+y_off), color)

    def regions(x, y, chosen):
        pixel_set((int(x*scale)+x_off, int(y*scale)+y_off), color[chosen])

    def fancy(x, y, chosen):
        pixel= (int(x*scale)+x_off, int(y*scale)+y_off)
        c = [0,0,0]
        global pixel_count
        if not pixel_count.has_key(pixel):
            c[color] = 50
            pixel_set(pixel,c)
            pixel_count[pixel] = 1
        else:
            pixel_count[pixel] += 1
            if pixel_count[pixel]*10>205:
                c[color] = 255
                pixel_set(pixel, c)
            else:
                c[color] = 50+10*pixel_count[pixel]
                pixel_set(pixel, c)

    draw_methods = [normal, regions, fancy]

    def speak_method(x, y, i):
        if not image:pygame.display.flip()
        message("%d%% done."%((float(i)/float(its))*100), V_ESSENTIAL)
                
    run_IFS(its, skip, rules, draw_methods[opts.color_type], speak_method, 1000)
    
    if image:
        screen.save(opts.save, "PNG")
        message("Saved image to %s"%opts.save, V_ESSENTIAL)
    else:
        message("Finished", V_ESSENTIAL)
