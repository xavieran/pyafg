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

from pyafg import make_gradient



if __name__ == "__main__":
    #Initialize the display and background
    pygame.init()
    display = pygame.display.set_mode((400,400))
    pygame.display.set_caption("Press a key to exit")
    pygame.display.flip()
    width = 1
    if not sys.argv[1:]:
        print "Demo, use to test out gradients. "
    i = [int(x) for x in sys.argv[1].split(',')]
    s = [int(x) for x in sys.argv[2].split(',')]
    e = [int(x) for x in sys.argv[3].split(',')]
    colors = make_gradient(i,s,e)
    y = 0
    for c in colors:
       pygame.draw.line(display, c, (0, y), (400, y), width)
       pygame.display.flip()
       y += 1

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT: sys.exit()
            if event.type == KEYDOWN: sys.exit()
        pygame.display.flip()

