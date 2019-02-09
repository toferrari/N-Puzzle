#!/usr/bin/env python3
# coding: utf-8

import sys
import argparse

import heuristics
import utils
from State import State
from parse import parse
from Game import Game


def helper():
	print ("Wrong enter.\n")
	print ("python3 N-Puzzle [-][option] [puzzle]")
	print ("\t-m : manhattan heuristic")
	print ("\t-v : graphic vision")


if __name__ == "__main__" :
	if (len(sys.argv) == 1 or len(sys.argv) > 3):
		helper()

	parser = argparse.ArgumentParser()

	parser.add_argument("-m", "--manhattan", action="store_true", default=False, help="Use manhattan heuristic.")
	parser.add_argument('file', type=argparse.FileType('r'))

	args = parser.parse_args()
	puzzle = parse(args.file)
	game = Game(utils._convert_to_dict(puzzle), len(puzzle))
	if game.is_solvable:
		game.solve()
	else:
		print("Cannot solve this n-puzzle.")
