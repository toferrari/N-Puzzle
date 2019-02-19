# coding: utf-8

from math import sqrt
from utils import get_key



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


def linear_conflict(state, final_state):
	ret = 0
	size = len(state)
	keys = list(state.keys())
	for index, key_j in enumerate(keys):
		if index + 1 < size:
			key_k = keys[index + 1]
			if state[key_j] != 0 and state[key_k] != 0 and key_k[1] == key_j[1]:
				goal_key_j = get_key(final_state, state[key_j])
				goal_key_k = get_key(final_state, state[key_k])
				if key_j[1] == goal_key_j[1] and key_k[1] == goal_key_k[1] and state[key_j] > state[key_k]:
					ret += 1
			key_k = (key_k[1], key_k[0])
			key_j = (key_j[1], key_j[0])
			if state[key_j] != 0 and state[key_k] != 0 and key_k[0] == key_j[0]:
				goal_key_j = get_key(final_state, state[key_j])
				goal_key_k = get_key(final_state, state[key_k])
				if key_j[0] == goal_key_j[0] and key_k[0] == goal_key_k[0] and state[key_j] > state[key_k]:
					ret += 1
	return manhattan(state, final_state) + 2 * ret


choices = {"manhattan": manhattan,
           "hamming": hamming,
		   "euclid": euclid,
		   "linear_conflict": linear_conflict
		   }
