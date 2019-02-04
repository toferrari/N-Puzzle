# coding: utf-8

def manhattan_distance(A, B):
	return abs(B['x'] - A['x']) + abs(B['y'] - A['y'])


def euclid_distance(A, B):
	return ((B['x'] - A['x'])**2 + (B['y'] - A['y'])**2)**1/2
