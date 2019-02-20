#!/usr/bin/python
#
# The Python Imaging Library
# $Id: taquin.py,v 1.1 2004/08/19 08:59:25 xof Exp xof $
#
#---------------
htile = 160
vtile = 160
hole=(0, 0) # (x, y)
#---------------
from random import randrange
from Tkinter import *
import Image, ImageTk

#
# an image viewer

class Cmdframe(Frame):
    def __init__(self):
        global filename
        Frame.__init__(self)
        self.strict = IntVar()
        quit = Button(self, text="Quit", command = sys.exit).pack(side = LEFT)
        quit = Button(self, text="Shuffle", command = shuffle).pack(side = LEFT)
	Checkbutton(self, text="Strict", variable=self.strict).pack(side = LEFT)
        v = IntVar()
        for size in (40, 80, 160):
            Radiobutton(self, text=size, variable=v, value=size).pack(side = LEFT)

        fname = StringVar()
        e = Entry(self, textvariable=fname).pack(side =RIGHT)
        fname.set(filename)

class Tile:
    def __init__(self, im, box):
            im = im.crop(box)
            self.image = ImageTk.PhotoImage(im)

def shuffle():
    global hole, nli, nco
    for i in range(20):
        move(randrange(0, nli, 1), randrange(0, nco, 1))

def move(li, co):
    global nli, nco, hole
    print "move(", li, ", ", co, ")\n"
    if ((0 <= li < nli) and (0 <= co < nco)): # sanity check
        if (not((hole[0] == co) and (hole[1] == li))):  # id.
            image = tile[present[co, li]].image
            can.create_rectangle(co * (htile+1), li * (vtile+1), (co+1)*(htile+1)-1, (li+1)*(vtile+1)-1, fill="red", outline="blue")
            can.create_image(hole[0] * (htile+1), hole[1] * (vtile+1), image=image, anchor=NW)
            present[hole], present[co, li] = present[co, li], present[hole]
            hole = (co, li)


def click(event):
    global hole
    x, y = event.x, event.y
    li, co = event.y / vtile, event.x / htile
    move(li, co)

def old(xx):
    image = tile[present[co, li]].image
    print event.x
    can.create_rectangle(co * (htile+1), li * (vtile+1), (co+1)*(htile+1)-1, (li+1)*(vtile+1)-1, fill="red", outline="blue")
    can.create_image(hole[0] * (htile+1), hole[1] * (vtile+1), image=image, anchor=NW)
    present[hole], present[co, li] = present[co, li], present[hole]
    hole = (co, li)

#
# script interface

if __name__ == "__main__":

    filename = sys.argv[1]
    root = Tk()
    root.title(filename)

    im = Image.open(filename)
    print im.size
    nli, nco = im.size[1]/vtile, im.size[0]/htile
    print "nli, nco", nli, nco
    cmdf = Cmdframe().pack()

    can = Canvas(root, height=im.size[1]+im.size[1]/vtile, width=im.size[0]+im.size[0]/htile, bg='blue')
    can.pack()
    print "can ", can.size
    tile = {}
    present = {}
    for co in range((im.size[0]+htile/2)/htile):
        for li in range((im.size[1]+vtile/2)/vtile):
            box = co * htile, li * vtile, (co+1) * htile, (li+1) * vtile
            tile[co, li] = Tile(im, box)         #.grid(column = co, row = li)
            present[co, li] = (co, li)
            can.create_image(co * (htile+1), li * (vtile+1), image=tile[co, li].image, anchor=NW)
    can.bind("", click)
    co, li = hole
    can.create_rectangle(co * (htile+1), li * (vtile+1), (co+1)*(htile+1)-1, (li+1)*(vtile+1)-1, fill="red", outline="red")

    root.mainloop()
