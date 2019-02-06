#!/usr/bin/env python3
# coding: utf-8

from Board import Board
from EnumMove import Move
import heuristics
from Node import Node

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

def solve(board):
	solved_board = Board.get_ordered(board.array)
	print(solved_board)
	print("--------------------")
	print(board)
	x, y = board.blank['x'], board.blank['y']
	nodes = list(map(lambda direction: init_node(direction, board, solved_board), Move))
	nodes = [node for node in nodes if node]
