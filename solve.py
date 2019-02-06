# coding: utf-8


from Board import Board
from EnumMove import Move
import heuristics


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


def solve(board):
	solved_board = Board.get_ordered(board.array)
	print(solved_board)
	print("--------------------")
	print(board)

	#List of nodes
	success = False
	closed_list = []
	open_list = [blank.board]
	while success == False and (len(open_list) > 0):
		min_node = get_min_eval_node(open_list)
		if board == solved_board:
			success = True
		else:
			closed_list.append(min_node)
			neighbour_nodes = expand(min_node)
			for node in neighbour_nodes:
				node.parent = min_node
				node_exists = node_in_list(closed_list, node)
				if node_exists == False:
					open_list.append(node)
		closed_list.append(min_node)
