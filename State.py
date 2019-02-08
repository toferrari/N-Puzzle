# coding: utf8


import numpy as np
from EnumMove import Move
from utils import _convert_to_dict

SNAIL_STATES = {
	3: [[1, 2, 3], [8, 0, 4], [7, 6, 5]],
	4: [[1, 2, 3, 4], [12, 13, 14, 5], [11, 0, 15, 6], [10, 9, 8, 7]],
	5: [[1, 2, 3, 4, 5], [16, 17, 18, 19, 6], [15, 24, 0, 20, 7], [14, 23, 22, 21, 8], [13, 12, 11, 10, 9]],
	6: [[1, 2, 3, 4, 5, 6], [20, 21, 22, 23, 24], [7, 19, 32, 33, 34, 25], [8, 18, 31, 0, 35, 26], [9, 17, 30, 29, 28, 27], [10, 16, 15, 14, 13, 12, 11]],
	7: [[1, 2, 3, 4, 5, 6, 7], [24, 25, 26, 27, 28, 29], [8, 23, 40, 41, 42, 43, 30], [9, 22, 39, 48, 0, 44, 31], [10, 21, 38, 47, 46, 45, 32], [11, 20, 37, 36, 35, 34, 33], [12, 19, 18, 17, 16, 15, 14, 13]],
	8: [[1, 2, 3, 4, 5, 6, 7, 8], [28, 29, 30, 31, 32, 33, 34], [9, 27, 48, 49, 50, 51, 52, 35], [10, 26, 47, 60, 61, 62, 53, 36], [11, 25, 46, 59, 0, 63, 54, 37], [12, 24, 45, 58, 57, 56, 55, 38], [13, 23, 44, 43, 42, 41, 40, 39], [14, 22, 21, 20, 19, 18, 17, 16, 15]]
}

NORMAL_STATES = {
	3: [[1, 2, 3], [4, 5, 6], [7, 8, 0]],
	4: [[1, 2, 3, 4], [12, 13, 14, 5], [11, 0, 15, 6], [10, 9, 8, 7]]
}

directions = {
	Move.UP: (-1, 0),
	Move.DOWN: (1, 0),
	Move.LEFT: (0, -1),
	Move.RIGHT: (0, 1)
}


class State():


	def __init__(self, state, size, g_x=0, h_x=0, direction=None, parent=None):
		self.size = size
		self.state = state
		self.g_x = g_x
		self.h_x = h_x
		self.f_x = self.g_x + self.h_x
		self.direction = direction
		self.parent = parent
		self.blank = self.find()


	def __eq__(self, other):
		if other == None:
			return False
		return self.state == other.state


	def find(self, value = 0):
		for (x, y), cell in self.state.items():
			if value == cell:
				return {"x": x, "y": y}


	def can_shift(self, direction=None):
		if self.direction != None:
			self.direction = direction
		return not ((self.direction == Move.UP and self.blank['y'] == 0)\
			or (self.direction == Move.DOWN and self.blank['y'] == self.size - 1) \
			or (self.direction == Move.LEFT and self.blank['x'] == 0)\
			or (self.direction == Move.RIGHT and self.blank['x'] == self.size - 1))


	def shift(self, direction):
		if (isinstance(direction, Move) == False):
			raise ValueError("Argument should be of type <enum Move>.")
		if self.can_shift(direction):
			x1, y1 = self.blank['x'], self.blank['y']
			for key, (y2, x2) in directions.items():
				if key == direction:
					y, x = y1 + y2, x1 + x2
					tmp_cell = self.state[(x1, y1)]
					self.state[(x1, y1)] = self.state[(x, y)]
					self.state[(x, y)] = tmp_cell
					break
		return self


	def calculate_heuristics(self, goal, heuristic):
		self.h_x = heuristic(self.state, goal.state)
		self.f_x = self.g_x + self.h_x


	@classmethod
	def to_final_puzzle(cls, array, size, how='snail'):
		if how == 'snail':
			return cls(_convert_to_dict(np.array(SNAIL_STATES[size]).reshape(size, size)), size)
		elif how == 'ordinary':
			return cls(_convert_to_dict(np.array(NORMAL_STATES[size]).reshape(size, size)), size)
		else:
			print("Give a right <how> state")
			exit()
