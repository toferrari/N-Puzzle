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


def expand(current):
	neighbours = [
		State(current.state.copy(),
		  size=current.size,
		  g_x=current.g_x + 1,
		  direction=direction,
		  parent=current
		).shift(direction)
		for direction in Move
	]
	return [neighbour for neighbour in neighbours if neighbour != current]


def output_result(closed_list, start_time, i, goal):
	end_time = time()
	print("Resolved !")
	moves = 0
	elem = None
	for elem in closed_list:
		if elem == goal:
			break
		elem = next(iter(closed_list))
	while elem != None:
		moves += 1
		print(_convert_to_array(elem.state, elem.size), "---> ", elem.g_x)
		elem = elem.parent
	print("Number of moves: ", moves)
	print("Number of loops: ", i)
	print("time n-puzzle {:.2f}s".format(float(end_time - start_time)))


def solve(start, goal):
	print("Goal :\n", goal.state)
	print("N-puzzle :\n", start.state)
	print()
	start_time = time()
	open_list = set([start])
	closed_list = set()
	current = None
	i = 0
	while len(open_list) > 0:
		i += 1
		current = get_min_eval_node(open_list)
		closed_list.add(current)
		# closed_list.append(current)
		open_list.remove(current)
		if current == goal:
			output_result(closed_list, start_time, i, goal)
			break
		neighbours = expand(current)
		for neighbour in neighbours:
			if neighbour in closed_list:
				continue
			neighbour.calculate_heuristics(goal, heuristics.manhattan)
			if neighbour not in open_list:
				open_list.add(neighbour)
				# open_list.append(neighbour)
			elif current.g_x + 1 <= neighbour.g_x:
				open_list.add(neighbour)
				# print(neighbour)
				# index = get_index(open_list, neighbour)
				# open_list[index] = neighbour
