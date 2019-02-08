# coding: utf-8
#
# def manhattan_distance(A, B):
# 	return abs(B['x'] - A['x']) + abs(B['y'] - A['y'])

def manhattan(state, final_state):
	def man(Ax, Bx, Ay, By):
		return abs(Bx - Ax) + abs(By - Ay)

	ret = 0
	for y, row in enumerate(state):
		for x, cell in enumerate(row):
			if cell != 0:
				other_cell = final_state.find(cell)
				ret += man(other_cell['x'], x, other_cell['y'], y)
	return ret


def hamming(state, final_state):
	n = 0
	for y, row in enumerate(state):
		for x, cell in enumerate(row):
			if cell != 0 and state[y][x] != final_state[y][x]:
				n += 1
	return n



def euclid_distance(A, B):
	return ((B['x'] - A['x'])**2 + (B['y'] - A['y'])**2)**1/2
