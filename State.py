# coding: utf8


import numpy as np
# from Game import Game
from EnumMove import Move
from EnumCost import Cost


directions = {
	Move.UP: (0, -1),
	Move.DOWN: (0, 1),
	Move.LEFT: (-1, 0),
	Move.RIGHT: (1, 0)
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

	def __le__(self, other):
		return self.f_x <= other.f_x

	def __lt__(self, other):
		return self.f_x < other.f_x

	def __ge__(self, other):
		return self.f_x >= other.f_x

	def __gt__(self, other):
		return self.f_x > other.f_x

	def __hash__(self):
		return hash(frozenset(self.state.items()))


	def __str__(self):
		def get_border(highest_int, size):
			ret = " +"
			ret += "+".join("-"*(highest_int + 2) for _ in range(self.size))
			ret += "+\n"
			return ret

		highest_int = len(str(self.state[max(self.state.keys(), key=lambda key:self.state[key])]))
		border = get_border(highest_int, self.size)
		ret = border
		for x in range(self.size):
			for y in range(self.size):
				ret += " | %-*i" % (highest_int - len(str(self.state[(x, y)])) + 1, self.state[(x, y)])
			ret += " |\n%s" % border
		return ret


	def _can_shift(self, direction):
		return not ((direction == Move.UP and self.blank['y'] == 0)\
			or (direction == Move.DOWN and self.blank['y'] == self.size - 1) \
			or (direction == Move.LEFT and self.blank['x'] == 0)\
			or (direction == Move.RIGHT and self.blank['x'] == self.size - 1))


	def find(self, value = 0):
		for (x, y), cell in self.state.items():
			if value == cell:
				return {"x": x, "y": y}


	def expand(self):
		neighbours = [
			State(self.state.copy(),
			  size=self.size,
			  g_x=self.g_x + 1,
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
			for key, (x2, y2) in directions.items():
				if key == direction:
					x, y = x1+ x2, y1 + y2
					tmp_cell = self.state[(x1, y1)]
					self.state[(x1, y1)] = self.state[(x, y)]
					self.state[(x, y)] = tmp_cell
					self.blank = {"x": x, "y": y}
					break
		return self

	def set_direction(self, other):
		for direction, (y, x) in directions.items():
			if other.blank['y'] - y == self.blank['y'] and other.blank['x'] -	 x == self.blank['x']:
				self.direction = direction
				break


	def calculate_heuristics(self, goal, heuristic, cost):
		if (cost != Cost.UNIFORM):
			self.h_x = heuristic(self.state, goal.state)
		if (cost == Cost.GREEDY):
			self.g_x = 0
		elif (cost == Cost.UNIFORM):
			self.h_x = 0
		self.f_x = self.g_x + self.h_x
