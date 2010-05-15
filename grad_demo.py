#!/usr/bin/env python
#
#       classes.py
#       
#       Copyright 2009 Unknown <xavieran@Le-Chateau>
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


import os
import sys

import pygame
from pygame.locals import *



if __name__ == "__main__":
    #Initialize the display and background
    pygame.init()
    display = pygame.display.set_mode((400,400))
    pygame.display.flip()
    width = 1
    r = g = b = 0
    ir = int(sys.argv[1])
    ig = int(sys.argv[2])
    ib = int(sys.argv[3])
    colors = []
    y = 0
    while (r < 255) and (g < 255) and (b < 255):
       pygame.draw.line(display, (r,g,b), (0, y), (400, y), width)
       pygame.display.flip()
       r+=ir
       g+=ig
       b+=ib
       y += width
       colors.append((r, g, b))

    raw_input("%s"%len(colors))

