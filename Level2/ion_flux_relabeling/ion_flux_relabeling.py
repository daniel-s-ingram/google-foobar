import math

#Recursively subtract either 2^n or 2^n-1, where n is floor(log2(child)), from child until child ends up as either
#1 or 2. If it ends up as 1, it is a left child; if it ends up as 2, it is a right child. Subtract 2^n if child is (2^m-1)
#or 2*(2^m-1) for some m, and subtract 2^n-1 otherwise.

#The parent of a right child is right_child+1
#The parent of a left child is left_child+2^level, where level is the height of the left_child in the tree
def find_parent(original, child, level, height):
	if child >= 2**height-1:
		return -1
	elif child == 1:
		return original+2**(level)
	elif child == 2:
		return original+1

	isCorrectValue = False
	for i in xrange(1,height+1):
		if child == (2**i-1) or child == (2*(2**i-1)):
			isCorrectValue = True
			break

	if isCorrectValue:
		child = child-(2**(math.floor(math.log(child, 2))))
	else:
		child = child-(2**(math.floor(math.log(child, 2)))-1)

	return find_parent(original, child, level, height)

def is_power_of_two(x, array):
	for i in xrange(len(array)):
		if x == array[i]:
			return True
	return False

def answer(h, q):
    # your code here
	p = [-1]*len(q)
	height = h
	array = [0]*height
	for i in xrange(height):
	    array[i] = 2**i

	if height == 1:
		return [-1]*len(q)
	else:
		for i in xrange(len(q)):
			node = q[i]
			#Determine the level of the child node
			while not is_power_of_two(node+1, array):
				node = node - (2**(math.floor(math.log(node, 2)))-1)
			
			level = math.log(node+1, 2)
			p[i] = find_parent(q[i], q[i], level, height)
	return p

if __name__ == '__main__':
	print answer(3, [7, 3, 5, 1])
	print answer(5, [19, 14, 28])

#Originally used these two classes to construct the perfect binary tree - this implementation worked, but it took up
#too much memory for large trees
class Node(object):
	def __init__(self, value):
		self.value = value
		self.left_child = None
		self.right_child = None
		self.parent = None
		self.level = None

	def add_left_child(self, node):
		self.left_child = node

	def add_right_child(self, node):
		self.right_child = node

	def add_parent(self, node):
		self.parent = node

	def add_level(self, level):
		self.level = level

class Tree(object):
	def build_right_from_node(self, parent, child, level):
		if parent is 0:
			pass
		elif (self.nodes[parent].right_child is None) and (level > 1) and (self.nodes[parent].level is not 1) and (self.nodes[child].parent is None):
			self.nodes[parent].add_right_child(child)
			self.nodes[parent].add_level(level)
			self.nodes[child].add_parent(parent)
			self.nodes[child].add_level(level-1)
			
			level = level-1
			
			self.build_right_from_node(child, child-1, level)
		elif level == 1:
			self.retreat(parent+1, child, level+1)

	def retreat(self, parent, child, level):
		try:
			level = self.nodes[parent].level

			if parent is 0:
				pass
			elif self.nodes[parent].left_child is None:
				self.build_left_from_node(parent, child, level)
			elif self.nodes[parent].level is not self.height:
				self.retreat(parent+1, child, level+1)

		except:
			print 'Error in retreat' 

	def build_left_from_node(self, parent, child, level):
		if parent is 0:
			pass
		elif (self.nodes[parent].right_child is None) and (level > 1) and (self.nodes[parent].level is not 1):
			self.build_right_from_node(parent, child, level)
		elif (self.nodes[parent].right_child is not None) and (level > 1) and (self.nodes[parent].level is not 1) and (self.nodes[child].parent is None):
			self.nodes[parent].add_left_child(child)
			self.nodes[child].add_parent(parent)
			self.nodes[child].add_level(level-1)
			
			level = level-1

			self.build_left_from_node(child, child-1, level)
		elif level == 1 or self.nodes[parent].level is 1:
			self.retreat(parent+1, child, level+1)

	def __init__(self, h):
		self.height = h
		self.n = 2**h-1

		try:
			self.nodes = [Node(i) for i in xrange(self.n+1)]
			self.build_right_from_node(self.n, self.n-1, self.height)
		except:
			print 'Error in __init__'