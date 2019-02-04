# coding: utf-8

def manhattan_distance(A={x: 0, y:0}, B={x:0, y:0}):
	return abs(B['x'] - A['x']) + abs(B['y'] - A['y'])


def euclid_distance(A={x: 0, y:0}, B={x:0, y:0}):
	return ((B['x'] - A['x'])**2 + (B['y'] - A['y'])**2)**1/2
