from constraints import *
from time import sleep
from PIL import Image, ImageDraw, ImageFont

white = "#FFFFFF"
black = "#000000"

fg = black
bg = white

font = ImageFont.truetype("RobotoFlex-Regular.ttf", 18)

scale = 16

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
		d.rectangle([
			(min_x + margin + self.x.value()*scale, min_y + margin + self.y.value()*scale),
			(min_x + margin + (self.x.value() + self.width.value())*scale, min_y + margin + (self.y.value() + self.height.value())*scale)
		], outline=fg)
		if self.name is not None:
			d.text(
				(min_x + margin +  + (self.x.value() + self.width.value()/2)*scale, min_y + margin + (self.y.value() + self.height.value()/2)*scale),
				self.name, fill=fg, anchor="mm", font=font)

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


livingroom = Room(name="Livingroom")
bedroom_1 = Room(name="Bedroom 1")
bedroom_2 = Room(name="Bedroom 2")

rooms = [
	livingroom,
	bedroom_1,
	bedroom_2
]

constraints = [
	EqualityConstraint(Product(livingroom.width, livingroom.height), Dimension(400)),
	EqualityConstraint(Product(bedroom_1.width, bedroom_1.height), Dimension(200)),
	EqualityConstraint(Product(bedroom_2.width, bedroom_2.height), Dimension(200)),
	EqualityConstraint(bedroom_1.height, bedroom_2.height),
	EqualityConstraint(Sum(bedroom_1.height, bedroom_2.height), livingroom.height),
	EqualityConstraint(bedroom_1.x, Sum(livingroom.x, livingroom.width)),
	EqualityConstraint(bedroom_2.x, bedroom_1.x),
	EqualityConstraint(bedroom_1.y, livingroom.y),
	EqualityConstraint(bedroom_2.y, Sum(bedroom_1.y, bedroom_1.height))
]

well_constrained = [constraint.check() for constraint in constraints]

while not all(well_constrained):
	for constraint in constraints:
		constraint.adjust()
	well_constrained = [constraint.check() for constraint in constraints]

print([room.x.value() for room in rooms])
print([room.x.value() + room.width.value() for room in rooms])

min_x = min([room.x.value() for room in rooms])
min_y = min([room.y.value() for room in rooms])
max_x = max([room.x.value() + room.width.value() for room in rooms])
max_y = max([room.y.value() + room.height.value() for room in rooms])

margin = 2 * scale

image_width = int((max_x - min_x) * scale + margin * 2)
image_height = int((max_y - min_y) * scale + margin * 2)

img = Image.new("RGB", (image_width, image_height), bg)
for room in rooms:
	print(room)
	room.draw(img)
img.save("house.png")
