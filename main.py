#!/usr/bin/env python3
# coding: utf-8

import sys
import argparse

from Board import Board
from EnumMove import Move
from solve import solve
from parse import parse


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
	board = Board(puzzle)
	solve(board)
