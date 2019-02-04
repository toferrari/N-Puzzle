# coding: utf-8


from Board import Board
from EnumMove import Move
import heuristics

def solve(board):
	solved_board = Board.get_ordered(board.array)
	print(solved_board)
	print("--------------------")
	print(board)
	x, y, _ = board.blank
	for direction in Move:
		if board.can_shift(direction):
			x, y = board.get_coordinates_if_moved(direction).values()
			value = board[y][x]
			distance = heuristics.manhattan_distance(
				board.blank,
				solved_board.find(board[y][x])
			)
			print("If blank shift({}) then, distance({}) = {}".format( direction, value, distance))
