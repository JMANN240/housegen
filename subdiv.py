from time import sleep
import numpy as np
from PIL import Image, ImageDraw
from random import gauss, choice
from math import dist

sqft = 1400

class Room:
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
	
	def draw(self, img):
		d = ImageDraw.Draw(img)
		d.rectangle([((img.width)/2+self.x, (img.height)/2+self.y), ((img.width)/2+self.x+self.w, (img.height)/2+self.y+self.h)])
		

def point(d, x, y):
	r = 3
	d.ellipse([(x-3,y-3), (x+3,y+3)], (255,255,255), (255,255,255))

w = 4 * (sqft**(1/2) + gauss(0, (sqft**(1/2))/2))
h = (4*sqft) / (w/4)
m = max(w, h)

img = Image.new("RGB", (int(m*1.5), int(m*1.5)), (0,0,0))

house = Room(-w/2, -h/2, w, h)
house.draw(img)

img.save("house.png")
