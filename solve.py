#!/usr/bin/env python3
# coding: utf-8

import numpy as np
from time import time
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


def output_result(closed_list, start_time):
	end_time = time()
	print("Resolved !")
	closed_list.sort(key=lambda node: node.g_x)
	moves = 0
	item = closed_list[-1]
	while item != None:
		moves += 1
		print(item.array, "---> ", item.g_x)
		item = item.parent
	print("Number of moves: ", moves)
	print("time n-puzzle {:.2f}s".format(float(end_time - start_time)))


def solve(initial_state, final_state):
	print("Goal :\n", final_state.array)
	print("N-puzzle :\n", initial_state.array)
	print()
	start_time = time()
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
			output_result(closed_list, start_time)
			break
		neighbours = expand(current, final_state)
		for neighbour in neighbours:
			neighbour.h_x = neighbour.calculate_heuristics(heuristics.manhattan)
			neighbour.f_x = neighbour.g_x + neighbour.h_x
			if neighbour not in closed_list and neighbour not in open_list:
				open_list.append(neighbour)
				# continue
			# if neighbour not in open_list:
			elif current.g_x + 1 <= neighbour.g_x:
				index = get_index(open_list, neighbour)
				if index != -1:
					open_list[index] = neighbour
				else:
					open_list.append(neighbour)
				if neighbour in closed_list:
					closed_list.remove(neighbour)
