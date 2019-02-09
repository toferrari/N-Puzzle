# coding: utf-8

from time import time

import heuristics
import utils
from EnumMove import Move
from State import State

class Game():


	def __init__(self, puzzle, size, heuristic=heuristics.manhattan):
		self._size = size
		self._start = State(puzzle, size)
		self._goal = State.to_final_puzzle(puzzle, size)
		self._heuristic = heuristic

		self._start.calculate_heuristics(self._goal, self._heuristic)
		self.is_solvable = self._is_solvable()

		self._start_time = time()
		self._max_states = 0
		self._total_states = 0
		self._n_loop = 0


	def __del__(self):
		if self.is_solvable:
			print("time n-puzzle {:.2f}s".format(time() - self._start_time))


	def _is_solvable(self):
		'''
			Source:
				- http://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html
				- https://math.stackexchange.com/questions/293527/how-to-check-if-a-8-puzzle-is-solvable
		'''
		def get_n_inversions(puzzle, size):
			ret = 0
			for i in range(size):
				if puzzle[i] == 0:
					continue
				for j in range(i + 1, size):
					if puzzle[j] != 0 and puzzle[j] < puzzle[i]:
						ret += 1
			return ret


		puzzle = utils._convert_to_array(self._start.state, self._size).flatten()
		sorted_puzzle = utils._convert_to_array(self._goal.state, self._size).flatten()
		size = len(puzzle)
		i1, i2 = get_n_inversions(puzzle, size), get_n_inversions(sorted_puzzle, size)
		return i1 % 2 == i2 % 2


	def _output_result(self):
		elem = next((node for node in list(self._closed_list) if node == self._goal), None)
		moves = -1
		while elem != None:
			moves += 1
			print(utils._convert_to_array(elem.state, elem.size), "---> ", elem.g_x)
			elem = elem.parent
		print("Resolved !")
		print("Number of moves: ", moves)
		print("Number of loops: ", self._n_loop)
		print("Time complexity: ", self._total_states)
		print("Space complexity: ", self._max_states)


	def solve(self):
		current = None
		self._open_list = set([self._start])
		self._closed_list = set()

		n_states = 1
		while n_states > 0:
			current = min(self._open_list, key=lambda node: node.f_x)
			self._open_list.remove(current)
			self._closed_list.add(current)
			if current == self._goal:
				break
			neighbours = current.expand()
			self._total_states += len(neighbours)
			for neighbour in neighbours:
				if neighbour in self._closed_list:
					continue
				neighbour.calculate_heuristics(self._goal, self._heuristic)
				self._open_list.add(neighbour)
			self._n_loop += 1
			n_states = len(self._open_list)
			self._max_states = max(n_states, self._max_states)
		self._output_result()
