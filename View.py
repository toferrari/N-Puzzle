#!/usr/bin/env python3
# coding: utf-8

from tkinter import *
from Game import *
from PIL import Image
from PIL import ImageTk

class View():

    def __init__(self, path, size_game, puzzle):
        self.image = Image.open(path)
        self.size_game = size_game
        self.size_image = self.image.size[0]
        self.puzzle = puzzle
        self.puzzle_split = []
        self.new_image = Image.new('RGB', (self.size_image + (3*self.size_game), self.size_image + (3*self.size_game)))
        self.puzzle_goal = Game.make_goal(self.size_game)

    def split(self):
        for y in range(self.size_game):
            for x in range(self.size_game):
                area = (x*self.size_image/self.size_game, y*self.size_image/self.size_game, (x+1)*self.size_image/self.size_game, (y+1)*self.size_image/self.size_game)
                self.puzzle_split.append(self.image.crop(area))

    def creat_puzzle(self):
        loop = 0
        for y in range(self.size_game):
            for x in range(self.size_game):
                tmp = self.puzzle[loop]
                if (tmp != 0):
                    self.new_image.paste(self.puzzle_split[tmp - 1], (round(x*self.size_image/self.size_game) + x*3, round(y*self.size_image/self.size_game) + y*3))
                loop += 1
