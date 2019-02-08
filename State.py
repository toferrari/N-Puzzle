# coding: utf8


import numpy as np
from EnumMove import Move

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


class State():

	def __init__(self, array, g_x=0, h_x=0, final_state=None, parent=None):
		self.size = len(array)
		self.array = array
		self.g_x = g_x
		self.h_x = h_x
		self.f_x = 0
		self.parent = parent
		self.final_state = final_state
		self.blank = self.find()


	def __eq__(self, other):
		if (other == None) or (self.size != other.size):
			return False
		return (self.array == other.array).all()


	def __getitem__(self, index):
		return self.array[index]

	def find(self, value = 0):
		for y, row in enumerate(self.array):
			for x, cell in enumerate(row):
				if cell == value:
					return {"x": x, "y": y}


	def can_shift(self, direction):
		if (isinstance(direction, Move) == False):
			raise ValueError("Argument should be of type <enum Move>.")
		return not ((direction == Move.UP and self.blank['y'] == 0)\
			or (direction == Move.DOWN and self.blank['y'] == self.size - 1) \
			or (direction == Move.LEFT and self.blank['x'] == 0)\
			or (direction == Move.RIGHT and self.blank['x'] == self.size - 1))


	def shift(self, direction):
		if (isinstance(direction, Move) == False):
			raise ValueError("Argument should be of type <enum Move>.")
		if self.can_shift(direction):
			x, y = self.blank['x'], self.blank['y']
			tmp = self.array[y][x]
			if direction == Move.UP:
				self.array[y][x] = self.array[y - 1][x]
				self.array[y - 1][x] = tmp
				self.blank['y'] -= 1
			elif direction == Move.DOWN:
				self.array[y][x] = self.array[y + 1][x]
				self.array[y + 1][x] = tmp
				self.blank['y'] += 1
			elif direction == Move.LEFT:
				self.array[y][x] = self.array[y][x - 1]
				self.array[y][x - 1] = tmp
				self.blank['x'] -= 1
			elif direction == Move.RIGHT:
				self.array[y][x] = self.array[y][x + 1]
				self.array[y][x + 1] = tmp
				self.blank['x'] += 1
		return self


	def calculate_heuristics(self, heuristic):
		return heuristic(self, self.final_state)


	@classmethod
	def to_final_puzzle(cls, array, how='snail'):
		size = len(array)
		if how == 'snail':
			return cls(np.array(SNAIL_STATES[size]).reshape(size, size))
		elif how == 'ordinary':
			return cls(np.array(NORMAL_STATES[size]).reshape(size, size))
		else:
			print("Give a right <how> state")
			exit()
