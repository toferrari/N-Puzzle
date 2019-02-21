import sys
import numpy as np
from error import error

def lamdba_remove_list_empty(line):
	return(list(filter(lambda word: word != "", line)))

def get_index(line):
	for x, word in enumerate(line):
		for letter in word:
			if letter == '#':
				return (x)
	return (0)

def remove_htag(line):
	try:
		index = get_index(line)
		if index > 0:
			line = line[:index]
	except:
		pass
	return(line)

def convert_int(word):
	try:
		number = int(word)
		return (number)
	except:
		return (-1)

def check_duplicate(puzzle, lines):
	zero = 0
	for y, row in enumerate(puzzle):
		for x, number in enumerate(row):
			if (number < 0):
				error ("wrong number in puzzle.")
			if (number == 0):
				zero +=1
			if (zero > 1):
				error("More than 2 blank.")
			for i in range(y, len(puzzle)):
				for j in range(x, len(puzzle)):
					if (i == y and j == x and number == puzzle[i][j]):
						pass
					elif (number == puzzle[i][j] and number != 0):
						error("error duplicate numbers.")
	if (zero == 0):
		error("No blank.")

def custom_isdigit(line):
	for letter in line:
		if (not letter.isdigit() and letter != ' '):
			return False
	return True

def check_order_number(puzzle):
	puzzle.sort()
	for index, number in enumerate(puzzle):
		if (index == len(puzzle) - 1):
			pass
		elif (index > 0 and puzzle[index] -1 != puzzle[index - 1]):
			error("Error number don't follow next by +1")

def get_puzzle(lines):
	needle = -1
	for index, line in enumerate(lines):
		try:
			needle = line.index('#')
			lines[index] = line[:needle].strip()
		except ValueError:
			continue
		finally:
			# print(needle, lines[index])
			if needle != 0 and not lines[index]:
				error("Empty line.")
			if (not custom_isdigit(lines[index])):
				error ("Got an invalid character")

	lines = list(map(lambda line : line.split(' '), lines))
	lines = list(map(lambda line : lamdba_remove_list_empty(line), lines))
	size = 0
	line_puzzle = 0
	for line in lines:
		if (not line):
			continue
		elif (len(line) == 1 and size == 0):
			size = convert_int(line[0])
			if size < 3 or np.isnan(size):
				error("Size invalid.")
			puzzle = np.array([0] * size ** 2).reshape(size,size)
		else:
			if (len(line) != size or line_puzzle >= size):
				error ("Size is different than numbers of rows.")
			for index, word, in enumerate(line):
				puzzle[line_puzzle][index] = convert_int(word)
			line_puzzle += 1
	if (size != line_puzzle):
		error ("Size is different than numbers of rows.")
	check_duplicate(puzzle, lines)
	check_order_number(puzzle.flatten())
	return puzzle
