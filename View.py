#!/usr/bin/env python3
# coding: utf-8

from tkinter import *
import tkinter as tk
from Game import *
from PIL import Image
from PIL import ImageTk
class View():


    def __init__(self, path, size_game, puzzle):
        self.image = Image.open(path)
        self.size_game = size_game
        self.size_image = self.image.size[0]
        self.puzzle = puzzle
        self.piece_puzzle = []
        self.new_image = Image.new('RGB', (self.size_image + (3*self.size_game), self.size_image + (3*self.size_game)))
        self.puzzle_goal = Game.make_goal(self.size_game)

    def split(self):
        loop = 0
        for y in range(self.size_game):
            for x in range(self.size_game):
                loop += 1
                x0, y0, x1, y1 = x*self.size_image/self.size_game, y*self.size_image/self.size_game, (x+1)*self.size_image/self.size_game, (y+1)*self.size_image/self.size_game
                area = (x0, y0, x1, y1)
                print (area)
                image = ImageTk.PhotoImage(self.image.crop(area))
                piece = {'image' : image,
                         'x' : round(x0),
                         'y' : round(y0),
                         'visible' : True}
                self.piece_puzzle.append(piece)
        self.piece_puzzle[0]['visible'] = False
        print (self.piece_puzzle)

    def create_puzzle(self, root):
        loop = 0
        self.canvas = tk.Canvas(root, width=self.size_image,
                                    height=self.size_image, background='black')
        # self.canvas.pack()
        self.canvas.pack()
        # self.canvas.grid()
        for y in range(self.size_game):
            for x in range(self.size_game):
                tmp = self.puzzle[loop]
        # for i in range(len(self.piece_puzzle)):
                self.piece_puzzle[tmp]['x'] = round(x*self.size_image/self.size_game) + x*3
                self.piece_puzzle[tmp]['y'] = round(y*self.size_image/self.size_game) + y*3
                if (self.piece_puzzle[tmp]['visible'] == True):
                    self.canvas.create_image(self.piece_puzzle[tmp]['x'],
                    self.piece_puzzle[tmp]['y'],
                    image=self.piece_puzzle[tmp]['image'],
                    anchor=NW)
                #     self.new_image.paste(self.piece_puzzle[tmp]['image'], (self.piece_puzzle[tmp]['x'],self.piece_puzzle[tmp]['y']))
                loop+=1
        # loop = 0
        # x = self.piece_puzzle[0]['x']
        # y = self.piece_puzzle[0]['y']
        # tmp = self.piece_puzzle[10]['image']
        #         if (tmp != 0):
        #             self.new_image.paste(self.puzzle_split[tmp - 1], (round(x*self.size_image/self.size_game) + x*3, round(y*self.size_image/self.size_game) + y*3))
        #         loop += 1
