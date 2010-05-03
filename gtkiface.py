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


class Window:
    def destroy(self,widget=None,data=None):gtk.main_quit()
    
    def expose_handler(self, widget, event) :
        w, h = widget.window.get_size()
        xgc = widget.window.new_gc()
        xgc.set_rgb_fg_color(gtk.gdk.color_parse("cyan"))
        if not self.have_drawn:
            rules = load_file("fractals/fern.frct")
            for i in generate_IFS(100000, rules):
                widget.window.draw_point(xgc, i[0]*40+110, i[1]*40+400)
            self.have_drawn=True

    def __init__(self):
        #The window...
        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('IFS')
        self.window.connect('destroy',self.destroy)
        
        self.vbox = gtk.VBox()
        self.window.add(self.vbox)

        width, height = 200,400
        self.drawing_area = gtk.DrawingArea()
        self.drawing_area.set_size_request(width, height)
        self.drawing_area.connect("expose-event", self.expose_handler)
        self.vbox.pack_start(self.drawing_area)
        
        self.have_drawn = False
        #self.drawing_area.set_size_request(width, height)

        #self.drawing_area.pack()
        


    def show(self):
        self.drawing_area.show()
        self.vbox.show()
        self.window.show()


def main():
    g = Window()
    g.show()
    gtk.main()
if __name__ == '__main__': main()
