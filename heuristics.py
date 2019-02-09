# coding: utf-8

from math import sqrt


def manhattan(state, final_state):
	ret = 0
	for (Ax, Ay), Acell in state.items():
		for (Bx, By), Bcell in final_state.items():
			if Acell != 0 and Acell == Bcell:
				ret += abs(Bx - Ax) + abs(By - Ay)
	return ret


def hamming(state, final_state):
	ret = 0
	for coord, Acell in state.items():
		if Acell != 0 and final_state[coord] != Acell:
			ret += 1
	return ret


def euclid(state, final_state):
	ret = 0
	for (Ax, Ay), Acell in state.items():
		for (Bx, By), Bcell in final_state.items():
			if Acell != 0 and Acell == Bcell:
				ret += sqrt((Bx - Ax)**2 + (By - Ay)**2)
	return ret


choices = {"manhattan": manhattan, "hamming": hamming, "euclid": euclid}
