# coding: utf-8

import numpy as np


def _convert_to_dict(array):
	map = {}
	for y, row in enumerate(array):
		for x, cell in enumerate(row):
			map[(x, y)] = cell
	return map


def _convert_to_array(dict, size):
	array = np.array([0] * size * size).reshape(size, size)
	for (x, y), value in dict.items():
		array[y][x] = value
	return array
