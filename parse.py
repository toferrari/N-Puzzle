import re
import sys
import argparse
import numpy as np

def helper():
	print ("Wrong enter.\n")
	print ("python3 N-Puzzle [-][option] [puzzle]")
	print ("\t-m : manhattan heuristic")
	print ("\t-v : graphic vision")

def lamdba_remove_list_empty(line):
	return(list(filter(lambda word: word != "", line)))

def get_puzzle(lines):
	lines = list(map(lambda line : re.sub("\n", "", line), lines))
	lines = list(map(lambda line : line.split(' '), lines))
	lines = list(map(lambda line: lamdba_remove_list_empty(line), lines))
	size = "a"
	for line in lines:
		print(line)
		if (line[0] == "#" or line[0] == '#\n'):
			pass
		elif (len(line) == 1):
			try:
				if not isinstance(size, str):
					exit()
				size = int(line[0])
				puzzle = np.array([0] * size ** 2).reshape(size,size)
			except:
				print("Puzzle error")
				exit()
		else:
			try:
				if (len(line) != size):
					exit()
			except:
				print("Puzzle error")
				exit()
	print (puzzle)

[return {"x": x, "y": y, "value": value} for x in a if x == 0]

def parse(arg_file):
	try:
		with arg_file as file:
			lines = file.readlines()
	except FileNotFoundError:
		exit()
	file.close()

	puzzle = get_puzzle(lines)

if __name__ == "__main__" :
	if (len(sys.argv) == 1 or len(sys.argv) > 3):
		helper()

	parser = argparse.ArgumentParser()

	parser.add_argument("-m", "--manhattan", action="store_true", default=False, help="Use manhattan heuristic.")
	parser.add_argument('file', type=argparse.FileType('r'))

	args = parser.parse_args()

	parse(args.file)
