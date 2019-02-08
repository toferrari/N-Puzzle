# coding: utf-8

from time import time
import numpy as np

import heuristics
from EnumMove import Move
from State import State
from utils import _convert_to_array

class Game():

	def __init__(self, puzzle, size, h=heuristics.manhattan):
		self.size = size
		self.start = State(puzzle, size)
		self.goal = State.to_final_puzzle(puzzle, size)
		self.heuristic = h
		self.start.calculate_heuristics(self.goal, self.heuristic)

		self.start_time = time()
		self.max_states = 0
		self.total_states = 0
		self.n_loop = 0


	def _output_result(self):
		self.end_time = time()
		elem = None
		for elem in self.closed_list:
			if elem == self.goal:
				break
			elem = next(iter(self.closed_list))
		moves = -1
		while elem != None:
			moves += 1
			print(_convert_to_array(elem.state, elem.size), "---> ", elem.g_x)
			elem = elem.parent
		print("Resolved !")
		print("Number of moves: ", moves)
		print("Number of loops: ", self.n_loop)
		print("Complexity in space: ", self.max_states)
		print("time n-puzzle {:.2f}s".format(float(self.end_time - self.start_time)))


	def _expand(self, current):
		neighbours = [
			State(current.state.copy(),
			  size=current.size,
			  g_x=current.g_x + 1,
			  direction=direction,
			  parent=current
			).shift(direction)
			for direction in Move
		]
		return [neighbour for neighbour in neighbours if neighbour != current]


	def solve(self):
		current = None
		self.open_list = set([self.start])
		self.closed_list = set()

		n_states = 1
		while n_states > 0:
			current = min(self.open_list, key=lambda node: node.f_x)
			self.closed_list.add(current)
			self.open_list.remove(current)
			if current == self.goal:
				self._output_result()
				break
			neighbours = self._expand(current)
			for neighbour in neighbours:
				if neighbour in self.closed_list:
					continue
				neighbour.calculate_heuristics(self.goal, self.heuristic)
				self.open_list.add(neighbour)
			self.max_states = n_states if self.max_states < n_states else self.max_states
			self.n_loop += 1
			n_states = len(self.open_list)


	def is_solvable(self):
		#TODO: Convert check_soluble() here
		return True
