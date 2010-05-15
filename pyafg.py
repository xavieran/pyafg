#!/usr/bin/env python
#
#       pyafg.py
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
#       MA 02110-1301, USA.#!/usr/bin/env python
#
#IFS affine fractal generator
#
import sys
from optparse import OptionParser

from libifs import *



global VERBOSITY
VERBOSITY = 1

V_SHOWSTOPPER = 0
V_ESSENTIAL = 1
V_NORMAL = 2
V_DEBUG = 3

COLOR_NORMAL = 0
COLOR_REGION = 1
COLOR_FANCY = 2 #Y'know, it's the, uh, one that makes the image look... gradual?
COLOR_GRADIENT = 3

def message(msg, importance, fd = None):
    if importance <= VERBOSITY:
        if fd:
            fd.write(msg)
        else:
            print msg

def verify_string(string, regex):pass

def split_int(s, inter):
    return [s[x:x+inter] for x in xrange(0, len(s), inter)]

def string2color(s):
    return [int(i) for i in split_int(s, 3)]

def make_gradient(ir, ig, ib):
    r = g = b = 0
    colors = []
    while (r < 255) and (g < 255) and (b < 255):
        colors.append((r, g, b))
        r+=ir
        g+=ig
        b+=ib
    return colors

def load_colors_from_file(file):
    fd = open(file)
    lines = fd.readlines()
    fd.close()
    return [string2color(x.strip()) for x in lines if not x[0] == '#']


def setup_parser():
    parser = OptionParser()
    parser.description = "%prog (pyafg is an affine fractal generator) is a utility"+\
        " to draw affine transformation fractals"+\
        " with or without a display. It uses PIL for image rendering, and pygame"+\
        " if you want to watch the fractal being drawn."
    parser.usage = "%prog [options] <fractal.frct>"
    parser.prog = "pyafg"
    parser.add_option("-s", "--scale", type = "int", default = 0,\
        help = "The scaling factor for your fractal. 100 is usually a good try")
    parser.add_option("-a", "--autocalc", action = "store_true", default = False,\
        help = "Print out autocalced dimensions and offsets for this scaling.")
    parser.add_option("--speak-int", type = "int", default = 10000,\
        help = "The cycles to wait before printing out progress")
    parser.add_option("-x", "--x-offset", type = "int", default = 0,\
        help = "x offset for the fractal. negative values allowed")
    parser.add_option("-y", "--y-offset", type = "int", default = 0,\
        help = "the y offset for the fractal. negative values allowed")
    parser.add_option("-G", "--geometry", type = "string", default = "",\
        help = "Size of the viewing window (or image). In WxH format. eg. 120x240")
    parser.add_option("-i", "--iterations", type = "int", default = 100000,\
        help = "The number of iterations to go through.")
    parser.add_option("--color-type", type = "int", default = COLOR_NORMAL,\
        help = "The type of coloring you want. Choices from COLOR_NORMAL (0),"+\
        "COLOR_REGION (1), COLOR_FANCY (2), or COLOR_GRADIENT (3)."+\
        "Check the man page for details.")
    parser.add_option("-r", "--red-int", type = "int", default = 0,\
        help = "The interval that the red goes up by in the gradient.")
    parser.add_option("-g", "--green-int", type = "int", default = 1,\
        help = "The interval that the green goes up by in the gradient.")
    parser.add_option("-b", "--blue-int", type = "int", default = 0,\
        help = "The interval that the blue goes up by in the gradient.")
    parser.add_option("--color", type = "string", default = "000255000",\
        help = "A RRRGGGBBB string for the color to be used. If color-type is"+\
        " 2, you'll need to give as many colors as there are rules in your fractal")
    parser.add_option("--color-file", type = "string", default = "",\
        help = "A file with RRRGGGBBB strings separated by newline. # is a comment character")
    parser.add_option("--add-alpha", action = "store_true", default = False,\
        help = "Interpret colors as RRRGGGBBBAAA. This may not work with pygame")
    parser.add_option("-o", "--save", type = "string", default = "",\
        help = "The file to save an image to. If this is set, the pygame display"+\
        " will not be shown, and the image generated will be saved to named file")
    parser.add_option("-q", "--quiet", action = "store_false",\
                      default = "verbosity", help = "No output")
    parser.add_option("--progress", action = "store_true", default = False)
    parser.add_option("-v", "--verbosity", action = "store", type = "int",\
                      default = 1)

    return parser


def main(argv):
    #width, height, iterations, skiplen, how to plot (PIL, pygame, GTK, both?)
    #scale, x and y offsets,
    parser = setup_parser()
    opts, args = parser.parse_args(argv)
    args = args[1:]
    #Begin parsing arguments
    #    global VERBOSITY
    VERBOSITY = opts.verbosity
    message("Beginning option parsing", V_DEBUG)
    scale = opts.scale
    if not scale:
        parser.error("argument -s/--scale is compulsory!")
    
    if not args:
        parser.error("must specify a .frct file to use!")
    rules = load_file(args[0])
    
    if opts.autocalc:
        dim, offsets = calculate_best_settings(rules, scale)
        print "Dimensions: %dx%d"%(dim[0],dim[1])
        print """Offsets: x: %d
         y: %d"""%(offsets[0],offsets[1])
        sys.exit(0)
        

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

    if opts.color_type == COLOR_GRADIENT:
        color = make_gradient(opts.red_int, opts.green_int, opts.blue_int)
        
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
    def normal(x, y, chosen):#THIS IS A HACK (DIM, ETC.)
        pixel_set((int(x*scale)+x_off, int(dim[1]-(y*scale))+y_off), color)

    def regions(x, y, chosen):
        pixel_set((int(x*scale)+x_off, int(dim[1]-(y*scale))+y_off), color[chosen])

    def fancy(x, y, chosen):
        pixel = (int(x*scale)+x_off, int(dim[1]-(y*scale))+y_off)
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

    def gradient(x, y, chosen):
        pixel = (int(x*scale)+x_off, int(dim[1]-(y*scale))+y_off)
        global pixel_count
        if not pixel_count.has_key(pixel):
            pixel_set(pixel,color[0])
            pixel_count[pixel] = 1
        else:
            pixel_count[pixel] += 1
            try:pixel_set(pixel, color[pixel_count[pixel]])
            except IndexError:pixel_set(pixel, color[-1])
            
    draw_methods = [normal, regions, fancy, gradient]
    draw = draw_methods[opts.color_type]
    
    for points in generate_IFS(its, skip, rules):
        x, y, chosen, i = points
        draw(x, y, chosen)
        if i%opts.speak_int == 0:
            if not image: pygame.display.flip()
            message("%d%% done."%((float(i)/float(its))*100), V_ESSENTIAL)

    if image:
        screen.save(opts.save, "PNG")
        message("Saved image to %s"%opts.save, V_ESSENTIAL)
    else:
        raw_input()
        message("Finished", V_ESSENTIAL)
        
if __name__ == "__main__":main(sys.argv)
    
