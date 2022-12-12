from time import sleep
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from random import gauss, choice
from math import dist, pi, sin, cos

font = ImageFont.truetype("RobotoFlex-Regular.ttf", 12)

bg = "#FFFFFF"
fg = "#000000"

img = Image.new("RGB", (1024, 1024), bg)

class Node:
	def __init__(self, name):
		self.name = name
		self.x = 0
		self.y = 0
		self.neighbors = []
	
	def draw(self, img, initiator=None):
		d = ImageDraw.Draw(img)
		for i, neighbor in enumerate(self.neighbors):
			if neighbor is not initiator:
				neighbor.x = self.x + 128 * cos(i * 2 * pi / len(self.neighbors))
				neighbor.y = self.y + 128 * sin(i * 2 * pi / len(self.neighbors))
				d.line([(self.x, self.y), (neighbor.x, neighbor.y)], fill=fg)
				neighbor.draw(img, initiator=self)
		d.ellipse([(self.x-32, self.y-32), (self.x+32, self.y+32)], outline=fg, fill=bg)
		d.text((self.x, self.y), self.name, anchor="mm", fill=fg, font=font)

class Bedroom(Node):
	def __init__(self, name):
		super().__init__(name)
		closet = Node("Closet")
		self.neighbors.append(closet)

class Graph:
	def __init__(self):
		self.nodes = []
		self.connections = []
	
	def add(self, node):
		self.nodes.append(node)
	
	def connect(self, node_1, node_2):
		self.connections.append((node_1, node_2))
		node_1.neighbors.append(node_2)
		node_2.neighbors.append(node_1)

	def draw(self, img):
		half_width = img.size[0] / 2
		half_height = img.size[1] / 2
		self.nodes[0].x = half_width
		self.nodes[0].y = half_height
		self.nodes[0].draw(img)

livingroom = Node("Livingroom")
kitchen = Node("Kitchen")
bedroom_1 = Bedroom("Bedroom 1")
bedroom_2 = Bedroom("Bedroom 2")
bathroom = Node("Bathroom")

g = Graph()
g.add(livingroom)
g.add(kitchen)
g.add(bedroom_1)
g.add(bedroom_2)

g.connect(livingroom, bedroom_1)
g.connect(livingroom, bedroom_2)
g.connect(livingroom, kitchen)
g.connect(livingroom, bathroom)

g.draw(img)

img.save("house.png")
