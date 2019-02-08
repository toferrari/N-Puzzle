#!/usr/bin/env python3
# coding: utf-8

import numpy as np

from Board import Board
from EnumMove import Move
from State import State
from node import Node
import heuristics


def get_min_eval_node(l, current):
	return min(l, key=lambda node: node.f_x)

def get_index(l, other):
	for index, item in enumerate(l):
		if item == other:
			return index
	return -1

def expand(current, final_state):
	neighbours = [
	State(current.array.copy(),
		  g_x=current.g_x + 1,
		  final_state=final_state,
		  parent=current
		).shift(direction)
		for direction in Move
	]
	neighbours = [neighbour for neighbour in neighbours if (neighbour.array != current.array).any()]
	return neighbours


def output_result(closed_list):
	print("Resolved !")


def solve(initial_state, final_state):
	print("Goal :\n", final_state.array)
	print("N-puzzle :\n", initial_state.array)
	print()

	open_list = [initial_state]
	closed_list = []
	current = None
	i = 0
	while len(open_list) > 0:
		i += 1
		current = get_min_eval_node(open_list, current)
		closed_list.append(current)
		open_list.remove(current)
		if current == final_state:
			output_result(closed_list)
			break
		neighbours = expand(current, final_state)
		for neighbour in neighbours:
			if neighbour in closed_list:
				continue
			neighbour.h_x = neighbour.calculate_heuristics(heuristics.manhattan)
			neighbour.f_x = neighbour.g_x + neighbour.h_x
			if neighbour not in open_list:
			# if not in_list(open_list, neighbour):
				open_list.append(neighbour)
			elif current.g_x + 1 <= neighbour.g_x:
				index = get_index(open_list, neighbour)
				open_list[index] = neighbour
