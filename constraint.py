from constraints import *
from time import sleep
from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype("RobotoFlex-Regular.ttf", 12)

scale = 8

class Room:
	def __init__(self, name=None, x=0, y=0, width=1, height=1):
		self.name = name
		self.x = Dimension(x)
		self.y = Dimension(y)
		self.width = Dimension(width)
		self.height = Dimension(height)
	
	def __repr__(self):
		return f"name: {self.name}\nx: {self.x.value()}\ny: {self.y.value()}\nwidth: {self.width.value()}\nheight: {self.height.value()}\n"
	
	def draw(self, img):
		d = ImageDraw.Draw(img)
		half_width = img.width / 2
		half_height = img.height / 2
		d.rectangle([
			(half_width + self.x.value()*scale, half_height + self.y.value()*scale),
			(half_width + (self.x.value() + self.width.value())*scale, half_height + (self.y.value() + self.height.value())*scale)
		], outline="#FFFFFF")
		if self.name is not None:
			d.text(
				(half_width + (self.x.value() + self.width.value()/2)*scale, half_height + (self.y.value() + self.height.value()/2)*scale),
				self.name, fill="white", anchor="mm", font=font)

class Dimension:
	def __init__(self, x):
		self.x = x

	def value(self):
		return self.x
	
	def set(self, x):
		self.x = x
	
	def scale(self, s):
		self.x *= s

class Sum:
	def __init__(self, *args):
		self.xs = args

	def value(self):
		v = 0
		for x in self.xs:
			v += x.value()
		return v

	def set(self, x):
		v = self.value()
		if v != 0:
			for sx in self.xs:
				sx.scale(x/v)
		else:
			for sx in self.xs:
				sx.scale(x/len(self.xs))
	
	def scale(self, s):
		for sx in self.xs:
			sx.scale(s)

class Product:
	def __init__(self, *args):
		self.xs = args

	def value(self):
		v = 1
		for x in self.xs:
			v *= x.value()
		return v
	
	def set(self, x):
		v = self.value()
		if v != 0:
			for sx in self.xs:
				sx.scale((x/v)**(1/2))
		else:
			for sx in self.xs:
				sx.set((x)**(1/2))
	
	def scale(self, s):
		for sx in self.xs:
			sx.scale(s)


kitchen = Room(name="Kitchen", width=14, height=10)
diningroom = Room(name="Dining Room")
livingroom = Room(name="Livingroom", width=10, height=16)
bedroom_1 = Room(name="Bedroom 1", width=5, height=5)
bedroom_2 = Room(name="Bedroom 2", width=4, height=3)
bathroom = Room(name="Bathroom", width=4, height=3)
pantry = Room(name="Pantry", width=4, height=3)

rooms = [
	kitchen,
	diningroom,
	livingroom,
	bedroom_1,
	bedroom_2,
	bathroom,
	pantry
]

constraints = [
	EqualityConstraint(Sum(bedroom_1.height, bedroom_2.height), Sum(livingroom.height, bathroom.height)),
	EqualityConstraint(bedroom_1.x, Sum(livingroom.x, livingroom.width)),
	EqualityConstraint(bedroom_1.y, livingroom.y),
	EqualityConstraint(bedroom_2.x, Sum(livingroom.x, livingroom.width)),
	EqualityConstraint(bedroom_2.y, Sum(bedroom_1.y, bedroom_1.height)),
	EqualityConstraint(Product(bedroom_1.width, bedroom_1.height), Dimension(100)),
	EqualityConstraint(Product(bedroom_2.width, bedroom_2.height), Dimension(100)),
	EqualityConstraint(bedroom_1.width, bedroom_2.width),
	EqualityConstraint(livingroom.x, Sum(diningroom.x, diningroom.width)),
	EqualityConstraint(livingroom.y, diningroom.y),
	EqualityConstraint(diningroom.y, Sum(kitchen.y, kitchen.height)),
	EqualityConstraint(diningroom.x, kitchen.x),
	EqualityConstraint(kitchen.width, Sum(diningroom.width, livingroom.width, Dimension(5))),
	EqualityConstraint(Product(kitchen.width, kitchen.height), Dimension(150)),
	EqualityConstraint(Product(diningroom.width, diningroom.height), Dimension(200)),
	EqualityConstraint(diningroom.height, Sum(livingroom.height, bathroom.height)),
	EqualityConstraint(bathroom.y, Sum(livingroom.y, livingroom.height)),
	EqualityConstraint(bathroom.x, livingroom.x),
	EqualityConstraint(Product(bathroom.width, bathroom.height), Dimension(40)),
	EqualityConstraint(bathroom.width, livingroom.width),
	EqualityConstraint(pantry.x, Sum(kitchen.x, kitchen.width)),
	EqualityConstraint(pantry.y, kitchen.y),
	EqualityConstraint(pantry.height, kitchen.height),
	EqualityConstraint(Sum(pantry.width, kitchen.width), Sum(diningroom.width, livingroom.width, bedroom_1.width))
]

well_constrained = [constraint.check() for constraint in constraints]

while not all(well_constrained):
	for constraint in constraints:
		constraint.adjust()
	well_constrained = [constraint.check() for constraint in constraints]

img = Image.new("RGB", (600, 600), (0,0,0))
for room in rooms:
	print(room)
	room.draw(img)
img.save("house.png")