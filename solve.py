#!/usr/bin/env python3
# coding: utf-8

import numpy as np

from Board import Board
from EnumMove import Move
from State import State
from node import Node
import heuristics

def init_node(direction, g_x, board, solved_board):
	if board.can_shift(direction):
		tmp = Board(board.array.copy())
		coord = board.get_coordinates_if_moved(direction)
		x, y = coord['x'], coord['y']
		tmp.shift(direction)
		node = Node(
			board[y][x],
			x, y,
			g_x,
			heuristics.manhattan_distance(tmp, solved_board),
			parent=None,
			direction=direction
		)
		return (node)


def is_neighbour(current, target):
	if (target.blank['x'] - 1 == current.blank['x'] and\
		target.blank['y'] == current.blank['y']) or\
		(target.blank['x'] + 1 == current.blank['x'] and\
		target.blank['y'] == current.blank['y']) or\
		(target.blank['y'] - 1 == current.blank['y'] and\
		target.blank['x'] == current.blank['x']) or\
		(target.blank['y'] + 1 == current.blank['y'] and\
		target.blank['x'] == current.blank['x']):
		return True
	return False


def get_min_eval_node(l, current):
	tmp = l
	ret = min(tmp, key=lambda node: node.f_x)
	if current != None and not is_neighbour(current, ret):
		tmp = [item for item in tmp if is_neighbour(current, item)]
		if len(tmp) > 0:
			ret = min(tmp, key=lambda node: node.f_x)
	return ret


def in_list(l, other):
	ret = [state for state in l if state == other]
	return len(ret) > 0

def get_index(l, other):
	for index, item in enumerate(l):
		if item == other:
			return index
	return -1

def expand(current, final_state):
	# nodes = list(map(lambda direction: init_node(direction, g_x, board, solved_board), Move))
	# nodes = [node for node in nodes if node]
	# return nodes
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
	u = None
	i = 0
	while len(open_list) > 0:
		i += 1
		u = get_min_eval_node(open_list, u)
		closed_list.append(u)
		open_list.remove(u)
		print("\nDEPTH ------------------------: {}\n".format(u.g_x), u.array, "\n----------------------")
		if u == final_state:
			output_result(closed_list)
			break
		neighbours = expand(u, final_state)
		for neighbour in neighbours:
			if neighbour in closed_list:
			# if in_list(closed_list, neighbour):
				continue
			neighbour.h_x = neighbour.calculate_heuristics(heuristics.manhattan)
			neighbour.f_x = neighbour.g_x + neighbour.h_x
			if neighbour not in open_list:
			# if not in_list(open_list, neighbour):
				open_list.append(neighbour)
			else:
				index = get_index(open_list, neighbour)
				if neighbour.g_x < open_list[index].g_x:
					open_list[index] = neighbour
					# open_list[index].g_x = neighbour.g_x
					# open_list[index].h_x = neighbour.h_x
					# open_list[index].f_x = neighbour.f_x
					# open_list[index].parent = neighbour.parent
