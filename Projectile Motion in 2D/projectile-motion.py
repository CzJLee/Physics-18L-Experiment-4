"""
Physics 18L - Experiment 4 - Day 2
Christian Lee
  
Professor: N. Whitehorn
TA: Teresa Le
Lab Date: Thursday, Oct 24, 2019
UCLA Physics Department

Required libraries: matplotlib, numpy

Projectile motion in 2D
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class ParticleBox: 
	def __init__(self, init_state = [[1, 0, 1, 1]], box_bounds = [-2, 2, -2, 2], ball_size = 16, mass=0.05, gravity=9.81):
		#init_state is an [N x 4] array, where N is the number of particles:
		#[[x1, y1, vx1, vy1],
		#[x2, y2, vx2, vy2], ...]

		#bounds is the size of the box: [xmin, xmax, ymin, ymax]

		#size is the size of the ball

		self.init_state = np.asarray(init_state, dtype=float) #If init_state is not an array of floats, convert into an array containing only floats. 
		self.m = mass * np.ones(self.init_state.shape[0]) #self.init_state.shape[0] returns the number of particles contained within init_state. np.ones proudces an array full of n 1's where n is the passed variable. The mass of all particles will be set to m. 
		self.size = ball_size #Set the size of the particle
		self.state = self.init_state.copy() #Shallow copy the initial state into state, which will store the updates states as the particle moves. 
		self.bounds = box_bounds
		self.g = gravity #Gravity
		self.collision_scaling_factor = self.size*10

	def step(self, dt):
		#Calculate new position using the current velocity. 
		#x_i+1 = x_i + v
		self.state[:, :2] += self.state[:, 2:] * dt

		#Calculate logic when particle hits a wall
		#If particle reaches a wall, keep velocity along axis of the wall constant, and multiply perpendicular velocity by -1. 
		for n in range(0, len(self.state)):
			if self.state[n][0] <= self.bounds[0] + self.size/self.collision_scaling_factor:
				#Particle bounces off left wall
				self.state[n][0] = self.bounds[0] + self.size/self.collision_scaling_factor
				self.state[n][2] *= -1
			if self.state[n][0] >= self.bounds[1] - self.size/self.collision_scaling_factor:
				#Particle bounces off right wall
				self.state[n][0] = self.bounds[1] - self.size/self.collision_scaling_factor
				self.state[n][2] *= -1
			if self.state[n][1] <= self.bounds[2] + self.size/self.collision_scaling_factor:
				#Particle bounces off bottom wall
				self.state[n][1] = self.bounds[2] + self.size/self.collision_scaling_factor
				self.state[n][3] *= -1
			if self.state[n][1] >= self.bounds[3] - self.size/self.collision_scaling_factor:
				#Particle bounces off top wall
				self.state[n][1] = self.bounds[3] - self.size/self.collision_scaling_factor
				self.state[n][3] *= -1

		#Apply gravity. 
		#Gravity is applied as a force independant of particle mass. v_y = - g * dt
		for n in range(0, len(self.state)):
			self.state[n][3] += -self.g * dt

#Set up initial state
#np.random.seed(0) #Set constant seed.
init_state = -0.5 + np.random.random((10, 4)) #Randomly Generate (# of particles, # of elements (4 required))
#All particle dimension start with a position and veloicty between (-0.5, 0.5) produced by a gaussain distribution about 0. 
init_state[:, :2] *= 3.9 #Multiply the starting position of each particle by 3.9. 

#Define the working box variable of ParticleBox class. 
box = ParticleBox(init_state)

#Define step size dt. 
fps = 60
dt = 1 / fps

#fig determines where the plot is drawn on the screen. 
fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
	#Adjust screen position
ax = fig.add_subplot(aspect='equal', autoscale_on=False, xlim=(-3.2, 3.2), ylim=(-2.4, 2.4))
	#Draw axes positions

#Createa variable particles that contain the position of the particles.
particles, = ax.plot([], [], 'bo', ms=box.size)

# rect is the box edge
rect = plt.Rectangle(box.bounds[::2], box.bounds[1] - box.bounds[0], box.bounds[3] - box.bounds[2], edgecolor="black", linewidth=2, facecolor="none")
#Rectangle(bottom left corner coordinates, width, height, ...)
ax.add_patch(rect)

#Initialize the first frame of the animation
def init():
	global box, rect
	particles.set_data([], [])
	#rect.set_edgecolor('none')
	return particles, rect

def animate(i):
	#Sequential animation step that the animation function uses. The iterable i is not used. 
	"""perform animation step"""
	global box, rect, dt, ax, fig
	box.step(dt) #Take one step forward in time (dt). This updates all particles in box.
	
	# update pieces of the animation
	#rect.set_edgecolor('k')
	particles.set_data(box.state[:, 0], box.state[:, 1])
	#particles.set_markersize(box.size)
	return particles, rect

animate_plot = animation.FuncAnimation(fig, animate, frames=600, interval=10, blit=True, init_func=init)
#particles and rect are the only objects that actually get plotted. 

plt.show()
