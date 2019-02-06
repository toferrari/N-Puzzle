# coding: utf-8

import numpy as np

from EnumMove import Move

class Board():

	def __init__(self, array):
		self.array = array
		self.size = len(array)
		self.blank = self.find()


	def __repr__(self):
		return "<Board() - size: {}>".format(self.size)


	def __str__(self):
		return "\n".join([(" ".join("%i"%value for value in row)) for row in self.array])


	def __len__(self):
		return self.size


	def __getitem__(self, index):
		return self.array[index]


	def __eq__(self, other):
		if (isinstance(other, Board) == False):
			raise ValueError("Argument should be of type <object Board>.")
		if self.size != other.size:
			return False
		else:
			return (self.array == other.array).all()


	def find(self, value = 0):
		for y, row in enumerate(self.array):
			for x, cell in enumerate(row):
				if cell == value:
					return {"x": x, "y": y, "value": value}


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
		if not self.can_shift(direction):
			raise ValueError("Cannot shift")
		else:
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


	def get_coordinates_if_moved(self, direction):
		x, y, _ = self.blank.values()
		if direction == Move.UP:
			y -= 1
		elif direction == Move.DOWN:
			y += 1
		elif direction == Move.LEFT:
			x -= 1
		elif direction == Move.RIGHT:
			x += 1
		return {'x': x, 'y': y}


	@classmethod
	def get_ordered(cls, array):
		size = len(array)
		flat_list = [value for row in array for value in row]
		flat_list.sort()
		flat_list = np.roll(flat_list, -1)
		ordered = [flat_list[size * i : size * (i + 1)] for i in range(size)]
		return cls(ordered)
