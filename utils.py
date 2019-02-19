# coding: utf-8

import numpy as np


def _convert_puzzle_to_dict(puzzle):
	map = {}
	for x, row in enumerate(puzzle):
		for y, cell in enumerate(row):
			map[(y, x)] = cell
	return map


def _convert_list_to_dict(list, size):
	map = {}
	for y in range(size):
		for x in range(size):
			map[(y, x)] = list[x * size + y]
	return map


def _convert_to_array(dict, size):
	array = np.array([0] * size * size).reshape(size, size)
	for (x, y), value in dict.items():
		array[y][x] = value
	return array


def get_key(dict, needle):
	for key, value in dict.items():
		if value == needle:
			return key
	return None
