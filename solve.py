#!/usr/bin/env python3
# coding: utf-8

from Board import Board
from EnumMove import Move
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


def update_direction(board, target):
	cell = board.find(target.number)
	if cell['y'] - 1 == board.blank['y'] and cell['x'] == board.blank['x']:
		target.direction = Move.DOWN
	elif cell['y'] + 1 == board.blank['y'] and cell['x'] == board.blank['x']:
		target.direction = Move.UP
	elif cell['x'] - 1 == board.blank['x'] and cell['y'] == board.blank['y']:
		target.direction = Move.RIGHT
	elif cell['x'] + 1 == board.blank['x'] and cell['y'] == board.blank['y']:
		target.direction = Move.LEFT
	else:
		target.direction = None


def get_min_eval_node(board, open_list):
	if (len(open_list) == 1):
		return open_list[0]
	else:
		l = [item for item in open_list if item.direction]
		return min(l, key=lambda node: node.f_x)


def node_in_list(closed_list, target):
	for node in closed_list:
		if  node.number == target.number:
			return node
	return None


def expand(board, solved_board, g_x):
	nodes = list(map(lambda direction: init_node(direction, g_x, board, solved_board), Move))
	nodes = [node for node in nodes if node]
	return nodes


def remove_in_list(list, target):
	return [item for item in list if target.number != item.number]


def add_in_list(l, target):
	for index, item in enumerate(l):
		if item.number == target.number:
			l[index] = target
			break
	l.append(target)


def solve(board):
	solved_board = Board.get_ordered(board.array)
	print(solved_board)
	print("--------------------")
	print(board)
	print("--------------------")

	success = False
	closed_list = []
	open_list = [Node(0, board.blank['x'], board.blank['y'], h_x=heuristics.manhattan_distance(board, solved_board))]
	i = 0
	while len(open_list) != 0:
		u = get_min_eval_node(board,open_list)
		print("Min =\n", u)
		open_list = remove_in_list(open_list, u)
		if u.direction:
			board.shift(u.direction)
		if board == solved_board:
			print(board)
			print("fini")
			break
		nodes = expand(board, solved_board, u.g_x + 1)
		for node in nodes:
			print(node)
			node.parent = u
			k1 = node_in_list(open_list, node)
			k2 = node_in_list(closed_list, node)
			if k1 == None and k2 == None:
				node.f_x = node.g_x + node.h_x
				add_in_list(open_list, node)
			if k1 != None and k1.f_x > node.f_x:
				add_in_list(open_list, node)
				open_list = remove_in_list(open_list, k1)
			if k2 != None and k2.f_x > node.f_x:
				add_in_list(open_list, node)
				closed_list = remove_in_list(closed_list, k2)
		for open in open_list:
			update_direction(board, open)
		add_in_list(closed_list, u)
		print(board, "\n")
		i += 1
