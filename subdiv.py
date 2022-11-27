from time import sleep
import numpy as np
from PIL import Image, ImageDraw
from random import gauss, choices, choice
from math import dist

sqft = 1400
scale = 1/4 # One pixel is scale inches

class Window:
	width = 3 * (1 / scale)
	outcropping = 4

	def __init__(self, wall, x):
		self.wall = wall
		self.x = x
	
	def draw(self, img):
		d = ImageDraw.Draw(img)
		if self.wall.vertical:
			center = self.wall.y1 + (self.wall.y2 - self.wall.y1) * self.x
			d.line([((img.width)/2+self.wall.x1-self.outcropping, (img.height)/2+center+self.width/2), ((img.width)/2+self.wall.x1+self.outcropping, (img.height)/2+center+self.width/2)])
			d.line([((img.width)/2+self.wall.x1-self.outcropping, (img.height)/2+center-self.width/2), ((img.width)/2+self.wall.x1+self.outcropping, (img.height)/2+center-self.width/2)])
		if self.wall.horizontal:
			center = self.wall.x1 + (self.wall.x2 - self.wall.x1) * self.x
			d.line([((img.width)/2+center+self.width/2, (img.height)/2+self.wall.y1+self.outcropping), ((img.width)/2+center+self.width/2, (img.height)/2+self.wall.y1-self.outcropping)])
			d.line([((img.width)/2+center-self.width/2, (img.height)/2+self.wall.y1+self.outcropping), ((img.width)/2+center-self.width/2, (img.height)/2+self.wall.y1-self.outcropping)])

class Wall:
	def __init__(self, x1, y1, x2, y2, exterior=False):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.vertical = self.x1 == self.x2
		self.horizontal = self.y1 == self.y2
		self.exterior = exterior
		self.windows = []
		if self.exterior and dist((self.x1, self.y1), (self.x2, self.y2)) > Window.width * 4:
			self.windows.append(Window(self, 0.5))
	
	def draw(self, img):
		d = ImageDraw.Draw(img)
		d.line([((img.width)/2+self.x1, (img.height)/2+self.y1), ((img.width)/2+self.x2, (img.height)/2+self.y2)])
		for window in self.windows:
			window.draw(img)

class Room:
	def __init__(self, house, x, y, w, h, exteriors=[False, False, False, False]):
		self.walls = []
		self.house = house
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.walls.append(Wall(x, y, x+w, y, exteriors[0]))
		self.walls.append(Wall(x+w, y, x+w, y+h, exteriors[1]))
		self.walls.append(Wall(x+w, y+h, x, y+h, exteriors[2]))
		self.walls.append(Wall(x, y+h, x, y, exteriors[3]))
	
	def area(self):
		return self.w * self.h

	def draw(self, img):
		for wall in self.walls:
			wall.draw(img)
	
	def hsub(self):
		self.house.rooms.remove(self)
		split = self.w / 2 + gauss(0, w/12)
		self.house.rooms.append(Room(self.house, self.x, self.y, split, self.h, [self.walls[0].exterior, False, self.walls[2].exterior, self.walls[3].exterior]))
		self.house.rooms.append(Room(self.house, self.x+split, self.y, self.w-split, self.h, [self.walls[0].exterior, self.walls[1].exterior, self.walls[2].exterior, False]))
		del self

	def vsub(self):
		self.house.rooms.remove(self)
		split = self.h / 2 + gauss(0, h/12)
		self.house.rooms.append(Room(self.house, self.x, self.y, self.w, split, [self.walls[0].exterior, self.walls[1].exterior, False, self.walls[3].exterior]))
		self.house.rooms.append(Room(self.house, self.x, self.y+split, self.w, self.h-split, [False, self.walls[1].exterior, self.walls[2].exterior, self.walls[3].exterior]))
		del self

class House:
	def __init__(self, w, h):
		self.rooms = []
		self.rooms.append(Room(self, -w/2, -h/2, w, h, exteriors=[True, True, True, True]))
		
	def draw(self, img):
		for room in self.rooms:
			room.draw(img)

def point(d, x, y):
	r = 3
	d.ellipse([(x-3,y-3), (x+3,y+3)], (255,255,255), (255,255,255))

w = (1/scale) * (sqft**(1/2) + gauss(0, (sqft**(1/2))/4))
h = ((1 / scale) * sqft) / (w * scale)
m = max(w, h)

frame = 2
img = Image.new("RGB", (int(m*frame), int(m*frame)), (0,0,0))

n_rooms = 5

house = House(w, h)
for _ in range(n_rooms-1):
	selected_room = choices(house.rooms, [room.area() for room in house.rooms])[0]
	# subtype = choice((Room.hsub, Room.vsub)) # Random subdivision type
	subtype = Room.hsub if selected_room.w > selected_room.h else Room.vsub # Square-ish subdivision type
	subtype(selected_room)

house.draw(img)

img.save("house.png")
