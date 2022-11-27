from time import sleep
import numpy as np
from PIL import Image, ImageDraw
from random import gauss, choice
from math import dist

img = Image.new("RGB", (512, 512), (0,0,0))

d = ImageDraw.Draw(img)

def point(d, x, y):
	r = 3
	d.ellipse([(x-3,y-3), (x+3,y+3)], (255,255,255), (255,255,255))

def sufficiently_distanced(x, y):
	for point in points:
		if abs(point[0]-x) < 32 and abs(point[1]-y) < 32:
			return False
	return True

points = []
n = 16
x = 256
y = 256
for i in range(n):
	while(not sufficiently_distanced(x, y)):
		x += choice((1, -1)) * gauss(24, 12)
		y += choice((1, -1)) * gauss(24, 12)
	point(d, x, y)
	points.append((x, y))

distances = [[0 for _ in range(n)] for _ in range(n)]

for i, point1 in enumerate(points):
	for j, point2 in enumerate(points):
		distances[i][j] = dist(point1, point2)

print(distances)

def smallest(distances):
	current_min = None
	current_min_row = None
	current_min_col = None
	for i in range(n-1):
		for j in range(i+1, n):
			d = distances[i][j]
			if (current_min is None or d < current_min) and d != 0:
				current_min = d
				current_min_row = i
				current_min_col = j
	return current_min, current_min_row, current_min_col

def full(adj):
	adjmat = np.array(adj)
	adjmat = adjmat + np.identity(n)
	stepped = np.linalg.matrix_power(adjmat, n-1)
	return np.all(stepped > 0)

adj = [[0 for _ in range(n)] for _ in range(n)]

while not full(adj):
	di, i, j = smallest(distances)
	print(di)
	adj[i][j] = 1
	adj[j][i] = 1
	for row in adj:
		print(''.join([' ' if a==0 else '*' for a in row]))
	distances[i][j] = 0
	d.line([points[i], points[j]], (255,255,255), 1)

img.save("house.png")
