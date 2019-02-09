#!/usr/bin/env python3
# coding: utf-8

import subprocess
import argparse
import re

import heuristics
import utils
from State import State
from Game import Game
from parse import get_puzzle


def parse(arg_file):
	with arg_file as file:
		lines = file.readlines()
	return lines


if __name__ == "__main__" :
	parser = argparse.ArgumentParser()
	h_choices = list(heuristics.choices.keys())
	parser.add_argument("--heuristic", choices=h_choices, default=h_choices[0], help="Set a heuristic function.")
	parser.add_argument("-s", "--size", type=int, default=3, help="Generate a n-puzzle of size")
	parser.add_argument('file', nargs='?', type=argparse.FileType('r'))
	args = parser.parse_args()

	if args.file:
		lines = [re.sub('\n', '', line) for line in parse(args.file)]
	else:
		command = "./Puzzle/npuzzle-gen.py -s {}".format(args.size)
		lines = subprocess.check_output(command, shell=True, universal_newlines=True)[:-1].split('\n')

	args.heuristic = heuristics.choices[args.heuristic]
	puzzle = get_puzzle(lines)
	print(puzzle)
	game = Game(utils._convert_to_dict(puzzle), len(puzzle), heuristic=args.heuristic)
	if game.is_solvable:
		game.solve()
	else:
		print("Cannot solve this n-puzzle.")
