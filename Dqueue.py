# coding: utf-8

from collections import deque


class Dqueue(deque):

	def sort(self):
		items = sorted([self.pop() for _ in range(len(self))])
		self.extend(items)
