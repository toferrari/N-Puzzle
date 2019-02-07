#!/usr/bin/env python3
# coding: utf-8

import numpy as np
from error import error

def in_order(puzzle):
	for nb in puzzle:
		if (nb != -1):
			return False
	return True

def swap(puzzle, x1, x2):
	# print (puzzle, x1, x2)
	tmp = puzzle[x1]
	puzzle[x1] = puzzle[x2]
	puzzle[x2] = tmp
	return (puzzle)

def check_soluble(board):
	size = len(board.array)
	value = (size - 1 - board.blank['x']) + (size - 1 - board.blank['y'])
	puzzle = board.array
	puzzle = puzzle.flatten()
	size = len(puzzle)
	puzzle = swap(puzzle, np.where(puzzle == 0)[0], size - 1)
	puzzle[size - 1] = -1
	size -= 1
	action = 0
	while (in_order(puzzle) == False):
		arg_max = puzzle.argmax()
		if (arg_max != size -1):
			puzzle = swap(puzzle, arg_max, size - 1)
			puzzle[size - 1] = -1
			size -= 1
			action += 1
		else:
			puzzle[size - 1] = -1
			size -= 1
	print (value, action)
	if ((value % 2 != 0 and action % 2 == 0) or (value % 2 == 0 and action % 2 != 0)):
		error("Cannot solve taquin!")
