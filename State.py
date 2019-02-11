# coding: utf8


import numpy as np
# from Game import Game
from EnumMove import Move


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


	def __hash__(self):
		return hash(frozenset(self.state.items()))


	def _can_shift(self, direction=None):
		if self.direction != None:
			self.direction = direction
		return not ((self.direction == Move.UP and self.blank['y'] == 0)\
			or (self.direction == Move.DOWN and self.blank['y'] == self.size - 1) \
			or (self.direction == Move.LEFT and self.blank['x'] == 0)\
			or (self.direction == Move.RIGHT and self.blank['x'] == self.size - 1))


	def find(self, value = 0):
		for (x, y), cell in self.state.items():
			if value == cell:
				return {"x": x, "y": y}


	def expand(self):
		neighbours = [
			State(self.state.copy(),
			  size=self.size,
			  g_x=self.g_x + 1,
			  direction=direction,
			  parent=self
			).shift(direction)
			for direction in Move
		]
		return [neighbour for neighbour in neighbours if neighbour != self]


	def shift(self, direction):
		if (isinstance(direction, Move) == False):
			raise ValueError("Argument should be of type <enum Move>.")
		if self._can_shift(direction):
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
