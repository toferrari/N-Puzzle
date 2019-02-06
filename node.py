# coding: utf-8

class Node():

	def __init__(self, number, x, y, g_x=0, h_x=0, parent=None, direction=None):
		self.number = number
		self.x = x
		self.y = y
		self.parent = parent
		self.direction = direction
		self.g_x = g_x
		self.h_x = h_x
		self.f_x = self.g_x + self.h_x


	def __repr__(self):
		return "Node({}): ({}, {})".format(self.number, self.x, self.y)


	def __str__(self):
		return " -------------------\n| Number: {}\n| x, y: ({},{}) \n| f_eval: {}\n| Direction: {}\n -------------------\
		".format(self.number, self.x, self.y, self.f_x, self.direction)
