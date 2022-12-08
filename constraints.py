class EqualityConstraint:
	def __init__(self, x1, x2, tolerance=0.0001):
		self.x1 = x1
		self.x2 = x2
		self.tolerance = tolerance
	
	def check(self):
		return abs(self.x1.value() - self.x2.value()) < self.tolerance
	
	def adjust(self):
		self.x1.set(self.x2.value())

class LessThanOrEqualToConstraint:
	def __init__(self, x1, max):
		self.x1 = x1
		self.max = max
	
	def check(self):
		return self.x1.value() <= self.max.value()
	
	def adjust(self):
		if self.x1.value() > self.max.value():
			self.x1.set(self.max.value())

class GreaterThanOrEqualToConstraint:
	def __init__(self, x1, min):
		self.x1 = x1
		self.min = min
	
	def check(self):
		return self.x1.value() >= self.min.value()
	
	def adjust(self):
		if self.x1.value() < self.min.value():
			self.x1.set(self.min.value())

class RationalConstraint:
	def __init__(self, x1, x2, max_ratio):
		self.x1 = x1
		self.x2 = x2
		self.max_ratio = max_ratio
	
	def check(self):
		return ((self.x1.value() / self.x2.value()) <= self.max_ratio) and ((self.x2.value() / self.x1.value()) <= self.max_ratio)
	
	def adjust(self):
		if self.x1.value() > self.x2.value():
			scale_factor = self.x2.value() / self.x1.value() * 0.1
			self.x1.scale(1 - scale_factor)
			self.x2.scale(1 + scale_factor)
		elif self.x1.value() < self.x2.value():
			scale_factor = self.x2.value() / self.x1.value() * 0.1
			self.x1.scale(1 + scale_factor)
			self.x2.scale(1 - scale_factor)