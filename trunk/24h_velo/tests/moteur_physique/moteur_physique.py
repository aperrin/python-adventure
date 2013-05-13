#-*- coding:utf-8 -*-

from numpy import random as np_random
import math

def check_boundaries(a, max_):
	if a < 0 : 
		return 0
	else : 
		return a

	if a > max_ : 
		return max_
	else :
		return a		

class point:
	""" contains the positions of a single point  
	while it his on the screen. """	
 
	def __init__(self, size_screen, dt, gx, gy):
		"""
		"""

		# screen size
		self.x_max, self.y_max = size_screen
		self.x_min, self.y_min = 0, 0
		
		# constants 
		self.t = 0
		self.gx, self.gy = gx, gy
		self.dt = dt

		#np_random initial position of the particle
		#np_random initial speed
		self.vmax = 50
		angle = np_random.uniform(0, 360)
		self.vx0, self.vy0 = self.vmax * math.cos(angle), self.vmax * math.sin(angle)

		tmp = np_random.normal(0.5*(self.x_max - self.x_min), self.x_max/10, 1)[0]
		if np_random.randint(0, 2) : 	
			self.x0 = check_boundaries(tmp, self.x_max)
			self.y0 = 0.01 # not 0 for the border protection
			self.vy0 = abs(self.vy0)
		else : 
			self.y0 = check_boundaries(tmp, self.y_max)
			self.x0 = 0.01
			self.vx0 = abs(self.vx0)
			self.vy0 = abs(self.vy0)*10
			


	
		print 'x0 : {0}, y0 : {1}'.format(self.x0, self.y0)		
		print 'vx0 : {0}, vy0 : {1}'.format(self.vx0, self.vy0)

		# list of the positions
		self.pos_x = []
		self.pos_y = []

	def is_visible(self, x, y) :
		""" says if the particle is still visible on the screen """
		res_x = (x > self.x_min) and (x < self.x_max)
		# print 'res_x : {0},  x : {1},  x_min : {2},   x_max:{3}'.format(res_x, x, self.x_min, self.x_max)
		res_y = (y > self.y_min) #and (y < self.y_max)
		return res_x and res_y


	def calc_positions(self) :
		"""computes the vector of positions of a 
		projectile given its speed and position"""
		x, y = self.x0, self.y0

		while self.is_visible(x, y) :
			x = 0.5 * self.gx * self.t**2 + self.vx0 * self.t + self.x0
			y = 0.5 * self.gy * self.t**2 + self.vy0 * self.t + self.y0
			
			self.t += self.dt
			self.pos_x.append(x)
			self.pos_y.append(y)
	

	def get_positions(self):
		self.calc_positions()		
		return self.pos_x, self.pos_y


if __name__ == '__main__' :
	gx, gy, dt = -9.81, 0, 0.01
	screen_size = 1000, 1000	
	p = point(screen_size, dt, gx, gy)

	print 'computing positions'
	pos_x, pos_y = p.get_positions()
	#print "x : ", pos_x
	#print 'y : ', pos_y		

	# import matplotlib as mpl
	import matplotlib.pyplot as plt	
	fig = plt.figure()
	ax = fig.add_subplot(111, xlim = (0, screen_size[0]), ylim = (0, screen_size[1]))
	ax.plot(pos_y, pos_x)
	plt.show()


