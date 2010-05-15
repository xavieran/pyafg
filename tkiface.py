from libifs import *

from Tkinter import *    
from tkFileDialog import *

import os

def validate_transform_entry(string):
    try:
        string = float(string)
    except ValueError:
        return False
    return True

class TransformEditor():
    def __init__(self, tfile = ''):
        self.window = Tk()
        self.file = tfile
        
        self.tr_canvas_width, self.tr_canvas_height = 300, 300
        self.im_canvas_width, self.im_canvas_height = 300, 300

        self.menubar = Menu(self.window)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.load_new)
        self.filemenu.add_command(label="Save", command=self.save_trans)
        self.filemenu.add_command(label="New", command=self.delete_all_transforms)
        self.filemenu.add_command(label="Exit", command=exit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        
        
        self.window.config(menu=self.menubar)     
        self.trans_edit = Frame(self.window)
        self.TransformFrame(self.trans_edit)
        self.trans_edit.grid(row=1, column=0)

        if self.file: self.initiate_rules()
        
        self.config = Frame(self.window)
        self.ConfigFrame(self.config)
        self.config.grid(row=1, column=1)  

        self.canvas_frame = Frame(self.window)
        self.tr_canvas = Canvas(self.canvas_frame,width=self.tr_canvas_width, height=self.tr_canvas_height)
        self.tr_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        #self.tr_canvas.grid(row = 0, column = 0)
        self.im_canvas = Canvas(self.canvas_frame,width=self.im_canvas_width, height=self.im_canvas_height)
        self.im_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        #self.im_canvas.grid(row = 0, column = 1)
        self.canvas_frame.grid(row = 0, column = 0)

        self.pack_widgets()

    def ConfigFrame(self, frame):
        self.scale_b = Entry(frame)
        self.scale_b.insert(0, '100')
        self.scale_b.grid(row=1, column = 0)
        
        self.iters_e = Entry(frame)
        self.iters_e.insert(0, '10000')
        self.iters_e.grid(row=0, column=0)

        self.run_b = Button(frame, text = "Run IFS", command = self.draw)
        self.run_b.grid(row=2, column=0)

        self.draw_rules_b = Button(frame, text = "Draw Rules", command = self.draw_rules)
        self.draw_rules_b.grid(row=3, column=0)

        self.clear_b = Button(frame, text = "Clear Canvas", command = self.clear_im_canvas)
        self.clear_b.grid(row=4, column=0)

    def TransformFrame(self, frame):        
        self.widgets = []
        self.widgets.append([Label(self.trans_edit, text=i) for i in 'a', 'b', 'c', 'd', 'e', 'f'])

        self.print_trans = Button(frame, text="Print Transforms", command=lambda: xprint(self.__str__))
        self.print_trans.grid(row=0, column=0)

        self.add_new_b = Button(frame, text="Add New Transform", command=self.add_new_transform)
        self.add_new_b.grid(row=0, column=1)


    def create_point(self, x, y, color, canvas):
        canvas.create_line(x, y, x+1, y+1, fill = color) 

    def draw_polygon(self, points, canvas):
        px, py = points[0][0], points[0][1]
        for p in points[1:]:
            canvas.create_line(px, py, p[0], p[1])
            px, py, = p[0], p[1]
        canvas.create_line(px, py, points[0][0], points[0][1])

    def draw_rules(self):
        self.clear_tr_canvas()
        xoff = self.tr_canvas_width/2
        yoff = self.tr_canvas_width/2
        scale = self.tr_canvas_width/5
        points = [(0,0),(1, 0), (1,1), (0, 1)]

        self.tr_canvas.create_line(self.tr_canvas_width/2, 0, self.tr_canvas_width/2, self.tr_canvas_height)
        self.tr_canvas.create_line(0, self.tr_canvas_height/2, self.tr_canvas_width, self.tr_canvas_height/2)
        #self.draw_polygon([(p[0] * scale + xoff, (self.canvas_height - (p[1] * scale + yoff))) for p in points])
        
        for r in self.transforms():
            tmp = [calculate_transform(p[0], p[1], r) for p in points]
            self.draw_polygon([(p[0] * scale + xoff, (self.tr_canvas_height - (p[1] * scale + yoff))) for p in tmp], self.tr_canvas)
            
        ##transform 4 points
        #plot it

    def delete_all_transforms(self):
        for i in self.widgets[1:]:
            for e in i:
                e.destroy()
        self.widgets = self.widgets[:1]

    def clear_tr_canvas(self):
        self.clear_canvas(self.tr_canvas)

    def clear_im_canvas(self):
        self.clear_canvas(self.im_canvas)
        
    def clear_canvas(self, canvas):
        canvas.delete(ALL)

    def load_new(self):
        self.file = askopenfilename()
        self.delete_all_transforms()
        self.initiate_rules()
 
    def save_trans(self):
        fd = asksaveasfile(mode='w',)
        fd.write(self.__str__())
        fd.close()
        
    
    def draw(self):
        scale = int(self.scale_b.get())
        iters = int(self.iters_e.get())
        rules = load_str(self.__str__())
        dim, offsets = calculate_best_settings(rules, scale)
        x_off, y_off = offsets
        for point in generate_IFS(iters, iters*.05, rules):
            self.create_point((point[0]*scale)+x_off, (self.im_canvas_height-((point[1]*scale)+x_off)), "green", self.im_canvas)

            
    def initiate_rules(self):
        rules = load_file(self.file)
        num = len(rules)
        self.add_new_transform()
        while len(self.widgets) - 1 < num:
            self.add_new_transform()
        i = 1
        for r in rules:
            j = r[1]
            c = 0
            for n in j:
                self.widgets[i][c].delete(0, END)
                self.widgets[i][c].insert(0, n)
                c += 1
            i += 1

    def add_new_transform(self):
        self.widgets.append([Entry(self.trans_edit) for i in range(0, 6)])
        for i in self.widgets[-1]: i.insert(0,'0.0')
        self.pack_widgets()

    def pack_widgets(self):
        i = 0
        start_row = 1
        while i < len(self.widgets):
            j = 0
            while j < len(self.widgets[i]):
                self.widgets[i][j].grid(row=i+start_row, column=j)
                j += 1
            i += 1

    def __str__(self):
        return "\n".join([",".join([str(e) for e in i]) for i in self.transforms()])


    def transforms(self):
        return [[float(e[0].get()), float(e[1].get()), float(e[2].get()), float(e[3].get()), float(e[4].get()), float(e[5].get())] for e in self.widgets[1:]]

    

j = TransformEditor()
mainloop()
