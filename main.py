#!/usr/bin/env python3
# coding: utf-8

import numpy as np
import subprocess
import argparse
import re

import heuristics
import utils
from State import State
from Game import Game
from parse import get_puzzle

from tkinter import *
import tkinter as tk
from View import View
from PIL import Image
from PIL import ImageTk

def parse(arg_file):
	with arg_file as file:
		lines = file.readlines()
	return lines


if __name__ == "__main__" :
	parser = argparse.ArgumentParser()
	h_choices = list(heuristics.choices.keys())
	parser.add_argument("--heuristic", choices=h_choices, default=h_choices[0], help="Set a heuristic function.")
	parser.add_argument("-s", "--size", type=int, default=3, help="Generate a n-puzzle of size")
	parser.add_argument("-m", "--max_size", type=int, default=32, help="Max size of OPEN list. Lower than 8 means no limit.\nThe higher the number, the higher the complexity will be.")
	parser.add_argument("-v", "--view", action="store_true", default=False, help="graphic visualization")
	parser.add_argument('file', nargs='?', type=argparse.FileType('r'))
	args = parser.parse_args()

	if args.file:
		lines = [re.sub('\n', '', line) for line in parse(args.file)]
	else:
		command = "./Puzzle/npuzzle-gen.py -s {}".format(args.size)
		lines = subprocess.check_output(command, shell=True, universal_newlines=True)[:-1].split('\n')

	args.heuristic = heuristics.choices[args.heuristic]
	puzzle = get_puzzle(lines)
	game = Game(utils._convert_puzzle_to_dict(puzzle), len(puzzle), heuristic=args.heuristic, max_size=args.max_size)
	print("Game is solvable ? {}".format("Yes" if game.is_solvable else "no"))
	print(game)
	if game.is_solvable:
		game.solve()
		game.print_results()
		if (args.view):
			root = Tk()
			path_pic = "pc.jpg"
			display = View(path_pic, game._size, utils._convert_puzzle_to_list(puzzle), root, game.get_winning_path())
			display.split()
			display.create_puzzle()
			root.mainloop()
