#!/usr/bin/env python
#
#       gtkiface.py
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

import sys
import pygtk
pygtk.require('2.0')
import gtk

from libifs import *


class TransformEditor(gtk.

class Window:
    def destroy(self,widget=None,data=None):gtk.main_quit()

    def __init__(self):
        #The window...
        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('IFS')
        self.window.connect('destroy',self.destroy)
        
        self.table = gtk.Table(1, 6, True)
        self.window.add(self.table)
        self.labels = []
        for i in ['a','b','c','d','e','f']:
            self.labels.append(gtk.Label(i))
        for i in range(6):
            self.table.attach(self.labels[i], i, i+1, 0, 1)
        self.entries = 


    def show(self):
        for i in self.labels:i.show()
        self.table.show()
        self.window.show()


def main():
    g = Window()
    g.show()
    gtk.main()
if __name__ == '__main__': main()
