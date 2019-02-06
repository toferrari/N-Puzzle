#!/usr/bin/env python3
# coding: utf-8

from Board import Board
from EnumMove import Move
from node import Node
import heuristics

def init_node(direction, board, solved_board):
	if board.can_shift(direction):
		coord = board.get_coordinates_if_moved(direction)
		x, y = coord['x'], coord['y']
		node = Node(
			board[y][x],
			x, y,
			None,
			heuristics.manhattan_distance(
				board.blank,
				solved_board.find(board[y][x])
			)
		)
		print()
		print (node.number, node.x, node.y)
		return (node)


def get_min_eval_node(open_list):
	if (len(open_list) == 1):
		return open_list[0]
	else:
		return min(open_list, key=lambda node: node.f_eval)


def node_in_list(closed_list, target):
	for node in closed_list:
		if  node.number == target.number and \
			node.f_value < target.f_value:
			return True
	return False


def expand(board, solved_board):
	x, y = board.blank['x'], board.blank['y']
	nodes = list(map(lambda direction: init_node(direction, board, solved_board), Move))
	nodes = [node for node in nodes if node]

def solve(board):
	solved_board = Board.get_ordered(board.array)
	print(solved_board)
	print("--------------------")
	print(board)

	#List of nodes
	success = False
	closed_list = []
	open_list = [board.blank]
	# while success == False and (len(open_list) > 0):
	min_node = get_min_eval_node(open_list)
	if board == solved_board:
		success = True
	else:
		closed_list.append(min_node)
		neighbour_nodes = expand(board, solved_board)
		# 	for node in neighbour_nodes:
		# 		node.parent = min_node
		# 		node_exists = node_in_list(closed_list, node)
		# 		if node_exists == False:
		# 			open_list.append(node)
		# closed_list.append(min_node)
