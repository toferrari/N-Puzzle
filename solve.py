#!/usr/bin/env python3
# coding: utf-8

import numpy as np
from time import time
from Board import Board
from EnumMove import Move
from State import State
from node import Node
import heuristics
from utils import _convert_to_array


def get_min_eval_node(l):
	return min(l, key=lambda node: node.f_x)


def get_index(l, other):
	for index, item in enumerate(l):
		if item == other:
			return index
	return -1


def expand(current, final_state):
	neighbours = [
		State(current.state.copy(),
		  size=current.size,
		  g_x=current.g_x + 1,
		  direction=direction,
		  final_state=final_state,
		  parent=current
		).shift(direction)
		for direction in Move
	]
	return [neighbour for neighbour in neighbours if neighbour != current]


def output_result(closed_list, start_time, i):
	end_time = time()
	print("Resolved !")
	closed_list.sort(key=lambda node: node.g_x)
	moves = 0
	item = closed_list[-1]
	while item != None:
		moves += 1
		print(_convert_to_array(item.state, item.size), "---> ", item.g_x)
		item = item.parent
	print("Number of moves: ", moves)
	print("Number of loops: ", i)
	print("time n-puzzle {:.2f}s".format(float(end_time - start_time)))


def solve(initial_state, final_state):
	print("Goal :\n", final_state.state)
	print("N-puzzle :\n", initial_state.state)
	print()
	start_time = time()
	open_list = [initial_state]
	closed_list = []
	current = None
	i = 0
	while len(open_list) > 0:
		i += 1
		current = get_min_eval_node(open_list)
		closed_list.append(current)
		open_list.remove(current)
		if current == final_state:
			output_result(closed_list, start_time, i)
			break
		neighbours = expand(current, final_state)
		for neighbour in neighbours:
			if neighbour in closed_list:
				continue
			neighbour.calculate_heuristics(heuristics.manhattan)
			if neighbour not in open_list:
				open_list.append(neighbour)
			elif current.g_x + 1 <= neighbour.g_x:
				index = get_index(open_list, neighbour)
				open_list[index] = neighbour
