# coding: utf-8
#
# def manhattan_distance(A, B):
# 	return abs(B['x'] - A['x']) + abs(B['y'] - A['y'])

def manhattan_distance(board, solved_board):
	# return abs(B['x'] - A['x']) + abs(B['y'] - A['y'])
	distances = []
	for y, row in enumerate(board):
		for x, cell in enumerate(row):
			other_cell = solved_board.find(cell)
			distances.append(
				abs(x - other_cell['x']) + abs(y - other_cell['y'])
			)
	return sum(distances)

def euclid_distance(A, B):
	return ((B['x'] - A['x'])**2 + (B['y'] - A['y'])**2)**1/2
