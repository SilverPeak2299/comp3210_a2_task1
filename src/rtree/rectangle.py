import math
from point import Point

from itertools import combinations

class Rectangle:
	x_min: float
	x_max: float
	y_min: float
	y_max: float

	data_list: list

	max_size: int

	def __init__(self, max_size):
		self.x_min = math.inf
		self.y_min = math.inf
		self.x_max = -math.inf
		self.y_max = -math.inf

		self.data_list = []

		self.max_size = max_size

	def insert(self, data):
		"""Recursive function that inserts new data into the tree,
		recursivly inserts any new rects that where made from a split"""

		# check if valid point insert position
		if self.is_leaf():
			return self.insert_point(data)

		# Finding the rectangle that will have the samllest area once current data is inserted
		best_rect = min(self.data_list, key=lambda r: r.test_area(data))

		# Inserting the rect into the tree, at the best place
		possible_new_rect = best_rect.insert(data)

		# If a split occured insert the new rectangle that was genrated
		if possible_new_rect is not None:
			return self.insert_rect(possible_new_rect)

		#reset the rect size
		self.resize()
		return None

	def insert_rect(self, data):
			"""Inserts a rectangle into itself, 
			in case of split it returns the new rectangle generated ready for insertion
			"""

			self.data_list.append(data)
			self.resize()

			#check if split is nessasry
			if len(self.data_list) > self.max_size:

				#Split
				max_dist = 0
				max_tuple = ()

				#Finding the seeds for the 2 new rects
				for r1, r2 in combinations(self.data_list, 2):
					dist = r1.rect_dist(r2)

					if dist >= max_dist:
						max_dist = dist
						max_tuple = (r1, r2)

				to_insert = [rect for rect in self.data_list if rect not in max_tuple]

				new_rect = Rectangle(self.max_size)
				new_rect.insert_rect(max_tuple[1])

				#removing old values from the list
				self.data_list.remove(max_tuple[1])
				for rect in to_insert:
					self.data_list.remove(rect)

				self.resize()
					 
				#inserting old values in the box that is smallest with thier presence
				for rect in to_insert:
					a1 = self.test_area(rect)
					a2 = new_rect.test_area(rect)

					if a1 < a2:
						self.insert_rect(rect)
					
					else:
						new_rect.insert_rect(rect)

				#returning the newly generated rectangle
				return new_rect
			
	def insert_point(self, data):
		"""inserts a point into itself, 
		in case of split it returns the new rectangle generated ready for insertion
		"""

		self.data_list.append(data)
		self.resize()

		# Testing to see if a split is nessecery
		if len(self.data_list) > self.max_size:

			# Split :(
			max_dist = 0
			max_tuple = ()

			#finding seeds for new rectangles
			for p1, p2 in combinations(self.data_list, 2):
				dist = p1.dist(p2)

				if dist > max_dist:
					max_dist = dist
					max_tuple = (p1, p2)
			
		
			to_insert = [p for p in self.data_list if p not in max_tuple]
			new_rect = Rectangle(self.max_size)
			new_rect.insert_point(max_tuple[1])
			
			self.data_list.remove(max_tuple[1])
			
			for point in to_insert:
				self.data_list.remove(point)

			self.resize()

			#inserting points in the better boxes
			for p in to_insert:
				a1 = self.test_area(p)
				a2 = new_rect.test_area(p)

				if a1 < a2:
					self.insert_point(p)
				
				else:
					new_rect.insert_point(p)
					
			return new_rect


	def resize(self):
		"calucates the size of the rectangles based on the size of the rectangles / placement of points held within"

		# if the rectangle contains rectangles
		if isinstance(self.data_list[0], Rectangle):
			for rect in self.data_list:
				if rect.x_min < self.x_min:
					self.x_min = rect.x_min

				if rect.x_max > self.x_max:
					self.x_max = rect.x_max

				if rect.y_min < self.y_min:
					self.y_min = rect.y_min

				if rect.y_max > self.y_max:
					self.y_max = rect.y_max

			return
			
		# If the rectangle contains rectangles
		for point in self.data_list:
			if point.x < self.x_min:
					self.x_min = point.x

			if point.x > self.x_max:
					self.x_max = point.x

			if point.y < self.y_min:
					self.y_min = point.y

			if point.y > self.y_max:
					self.y_max = point.y

	def area(self):
		"returns the area idk why I made this but I used it for checking the inital stuff was working"
		return (self.x_max - self.x_min) * (self.y_max - self.y_min)
	
	def test_area(self, data):
		"non destructive form of resize that takes in a possible rect/point and returns what the new area would be"
		
		# if adding a rectangle
		if isinstance(data, Rectangle):
			x_min = min(self.x_min, data.x_min)
			x_max = max(self.x_max, data.x_max)
			y_min = min(self.y_min, data.y_min)
			y_max = max(self.y_max, data.y_max)

			return (abs(x_max - x_min)) * (abs(y_max - y_min))
		
		# assuming the data is a point
		x_min = min(self.x_min, data.x)
		x_max = max(self.x_max, data.x)
		y_min = min(self.y_min, data.y)
		y_max = max(self.y_max, data.y)

		return (abs(x_max - x_min)) * (abs(y_max - y_min))


	def dist_from(self, x, y):
		"""Distance from a given point"""

		x = max(self.x_min - x, 0, x - self.x_max)
		y = max(self.y_min - y, 0, y- self.y_max)

		return math.sqrt(x**2 + y**2)
	
	def rect_dist(self, rect) -> float:
		"distance from a given rectangle"

		x = max(self.x_min - rect.x_max, 0, rect.x_min - self.x_max)
		y = max(self.y_min - rect.y_max, 0, rect.y_min - self.y_max)

		return math.sqrt(x**2 + y**2)
	
	def is_leaf(self):
		"""does this recttangle contain points?"""
		try:
			return not isinstance(self.data_list[0], Rectangle)
		
		except(IndexError):
			return True



if __name__ == "__main__":
	# rect = Rectangle(3)
	# rect.insert_point(Point(1, 1.2, 3.4))
	# print(rect.area())
	# rect.insert_point(Point(2, 5, 9))
	# print(rect.area())
	# rect.insert_point(Point(3, 2, 1))
	# print(rect.area())
	# possible_rec = rect.insert_point(Point(4, 10, 11))

	# for point in rect.data_list:
	# 	print(point.id)

	# print("new rec")
	# for p in possible_rec.data_list:
	# 	print(p.id)

	#print(possible_rec.data_list)


	rect = Rectangle(3)
	rect.insert_rect(Rectangle(3))
	rect.insert_rect(Rectangle(4))
	rect.insert_rect(Rectangle(5))
	possible_rec = rect.insert_rect(Rectangle(6))

	print("hey")