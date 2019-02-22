# coding: utf-8

from time import time
import numpy as np

import heuristics
import utils
from heapq import heappop, heappush, nlargest, nsmallest, heapify
from EnumMove import Move
from State import State, directions

class Game():


	def __init__(self, puzzle, size, heuristic=heuristics.manhattan, max_size=8):
		self._size = size
		self._max_size = max_size if max_size > 8 else 0
		self._start = State(puzzle, size)
		goal = Game.make_goal(size)
		self._goal = State(utils._convert_list_to_dict(goal, size), size)
		self._heuristic = heuristic

		self._start.calculate_heuristics(self._goal, self._heuristic)
		self.is_solvable = self._is_solvable()

		self._start_time = time()
		self._max_states = 0
		self._total_states = 0
		self._n_loop = 0
		self.results = None

		self._open_heap = []

	def __str__(self):
		return "Puzzle: \n%s" % self._start


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
					if puzzle[j] != 0 and puzzle[i] > puzzle[j]:
						ret += 1
			return ret

		puzzle = utils._convert_to_array(self._start.state, self._size).flatten()
		sorted_puzzle = utils._convert_to_array(self._goal.state, self._size).flatten()
		size = len(puzzle)
		i1 = get_n_inversions(puzzle, size) + (list(puzzle).index(0) if self._size % 2 == 0 else 0)
		i2 = get_n_inversions(sorted_puzzle, size) + (list(sorted_puzzle).index(0) if self._size % 2 == 0 else 0)
		return i1 % 2 == i2 % 2


	def _generate_results(self):
		self.results = []
		elem = next((node for node in list(self._closed_list) if node == self._goal), None)
		while elem != None:
			if elem.parent:
				self.results.append(elem.parent)
			elem = elem.parent
		self.results.reverse()
		size = len(self.results)
		[result.set_direction(self._goal)\
			if index + 1 == size\
			else result.set_direction(self.results[index + 1])\
		for index, result in enumerate(self.results)]
		if self.is_solvable:
			print("time n-puzzle {:.2f}s".format(time() - self._start_time))


	def _pop_max(self, size):
		n = size - self._max_size
		if self._max_size < 0 or n < 1:
			return
		to_delete = nlargest(n, self._open_heap)
		self._open_heap = [x for x in self._open_heap if x not in to_delete]
		heapify(self._open_heap)


	def solve(self):
		current = None
		heappush(self._open_heap, self._start)
		self._closed_list = set()

		n_states = 1
		while n_states > 0:
			current = heappop(self._open_heap)
			self._closed_list.add(current)
			if current == self._goal:
				break
			neighbours = current.expand()
			self._total_states += len(neighbours)
			for neighbour in neighbours:
				if neighbour in self._closed_list:
					continue
				neighbour.calculate_heuristics(self._goal, self._heuristic)
				heappush(self._open_heap, neighbour)
			self._n_loop += 1
			n_states = len(self._open_heap)
			self._pop_max(n_states)
			self._max_states = max(self._max_size if self._max_size else n_states, self._max_states)
		self._generate_results()


	def _print_states_in_file(self, filename="results.txt"):
		try:
			with open(filename, 'w') as f:
				for result in self.results:
					f.write("%s\n"%result)
				f.write("%s\n"%self._goal)

		except PermissionError:
			print("Error: Could not write in file: %s"%filename)


	def print_results(self):
		to_print = {
		 "Number of moves: ": len(self.results),
		 "Number of loops: ": self._n_loop,
		 "Time complexity: ": self._total_states,
		 "Size complexity: ": self._max_states
		}
		print("\n".join("%s%s" % (key, value) for (key, value) in to_print.items()))
		self._print_states_in_file()

	def get_winning_path(self):

		def moving_number(result):
			for direction, (y, x) in directions.items():
				if result.direction == direction:
					return result.state[(result.blank['x'] + x, result.blank['y'] + y)]

		if self.results == None:
			return None
		return [(result.direction, moving_number(result)) for result in self.results]


	@staticmethod
	def make_goal(s):
		ts = s*s
		puzzle = [-1 for i in range(ts)]
		cur = 1
		x = 0
		ix = 1
		y = 0
		iy = 0
		while True:
			puzzle[x + y*s] = cur
			if cur == 0:
				break
			cur += 1
			if x + ix == s or x + ix < 0 or (ix != 0 and puzzle[x + ix + y*s] != -1):
				iy = ix
				ix = 0
			elif y + iy == s or y + iy < 0 or (iy != 0 and puzzle[x + (y+iy)*s] != -1):
				ix = -iy
				iy = 0
			x += ix
			y += iy
			if cur == s*s:
				cur = 0

		return puzzle
