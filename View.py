#!/usr/bin/env python3
# coding: utf-8

from tkinter import *
import tkinter as tk
from Game import *
from EnumMove import Move
from PIL import Image
from PIL import ImageTk
from PIL import ImageGrab
from error import error

class View():


    def __init__(self, path, size_game, puzzle, root, way):
        try:
            self.image = Image.open(path)
            self.image = self.image.resize((1024, 1024), Image.ANTIALIAS)
            self.size_game = size_game
            self.size_image = self.image.size[0]
            self.puzzle = puzzle
            self.canvas = tk.Canvas(root, width=self.size_image,
                                        height=self.size_image, background='white')
            self.canvas.pack()
            self.piece_puzzle = [0]*self.size_game**2
            self.puzzle_goal = Game.make_goal(self.size_game)
            self.way = way
            self.n_move = 0
            self.create_events()
        except:
            error("Error : could not open image: %s"%path)

    def split(self):
        loop = 0
        for y in range(self.size_game):
            for x in range(self.size_game):
                loop += 1
                x0, y0, x1, y1 = x*self.size_image/self.size_game, y*self.size_image/self.size_game, (x+1)*self.size_image/self.size_game, (y+1)*self.size_image/self.size_game
                area = (x0, y0, x1, y1)
                image = ImageTk.PhotoImage(self.image.crop(area))
                piece = {'id_canvas' : None,
                         'image' : image,
                         'x' : round(x0),
                         'y' : round(y0),
                         'visible' : True}
                self.piece_puzzle[self.puzzle_goal[y * self.size_game + x]] = piece
        self.piece_puzzle[0]['visible'] = False

    def create_puzzle(self):
        loop = 0
        for y in range(self.size_game):
            for x in range(self.size_game):
                index = self.puzzle[loop]
                self.piece_puzzle[index]['x'] = round(x*self.size_image/self.size_game)
                self.piece_puzzle[index]['y'] = round(y*self.size_image/self.size_game)
                if (self.piece_puzzle[index]['visible'] == True):
                    tmp = self.canvas.create_image(self.piece_puzzle[index]['x'],
                    self.piece_puzzle[index]['y'],
                    image=self.piece_puzzle[index]['image'],
                    anchor=NW)
                    self.piece_puzzle[index]['id_canvas'] = tmp
                loop+=1

    def create_events(self):
        self.canvas.bind_all('<KeyPress-space>', self.move_puzzle)
        self.canvas.bind_all('<KeyPress-Escape>', self.move_puzzle)

    def _update_coordinates(self, piece):
        self.piece_puzzle[piece]['y'], self.piece_puzzle[0]['y'] =\
        self.piece_puzzle[0]['y'], self.piece_puzzle[piece]['y']
        self.piece_puzzle[piece]['x'], self.piece_puzzle[0]['x'] =\
        self.piece_puzzle[0]['x'], self.piece_puzzle[piece]['x']

    def move_puzzle(self, event):
        if (event.keysym == 'Escape'):
            error("You press Escape in game.")
        index = self.n_move
        if (index >= len(self.way)):
            return
        move = self.way[index][0]
        piece = self.way[index][1]
        if (move == Move.UP or move == Move.DOWN):
            coor = (0, self.piece_puzzle[0]['y'] - self.piece_puzzle[piece]['y'])
            self.canvas.move(self.piece_puzzle[piece]['id_canvas'], *coor)
        elif (move == Move.RIGHT or move == Move.LEFT):
            coor = (self.piece_puzzle[0]['x']-self.piece_puzzle[piece]['x'], 0)
            self.canvas.move(self.piece_puzzle[piece]['id_canvas'], *coor)
        self._update_coordinates(piece)
        self.n_move += 1
