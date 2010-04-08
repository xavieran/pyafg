
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


import pygame
import pygame.draw as dr
from pygame.locals import *

import libifs
import sys


dim = (800, 600)
screen = pygame.display.set_mode(dim)

screen.fill((255,255,255))
dr.line(screen, (0,0,0), (dim[0]/2, 0),(dim[0]/2,dim[1]), 3)
dr.line(screen, (0,0,0), (0, dim[1]/2),(dim[0],dim[1]/2), 3)

def offset_points(p, o):
    return [(i[0]+o[0],i[1]+o[1]) for i in p]
    
def scale_points(p, s):
    return [(i[0]*s, i[1]*s) for i in p]
    
def transform_points(p, tr):
    return [libifs.calculate_transform(i[0],i[1],tr) for i in p]

    
points = [(0,0), (1,0),(1,1),(0,1)]
width = 5
scale = 128
offset = (dim[0]/2, dim[1]/2 - scale)
transforms = libifs.load_file(sys.argv[1])

dr.polygon(screen, (255,0,0), offset_points(scale_points(points, scale), offset), 1)
for i in range(0,len(transforms)):
    dr.polygon(screen, (0,255,0), offset_points(scale_points(transform_points(points, transforms[i][1]), scale), offset), 2)

pygame.display.flip()
raw_input()
