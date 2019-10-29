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
from math import sqrt

from main import *

class ParticleBox: 
	def __init__(self, init_state = [[1, 0, 1, 1]], box_bounds = [-2, 2, -2, 2], ball_size=16, mass=0.05, gravity=[0, 10], drag=0, central_force = False, central_force_power=1):
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
		self.drag = drag
		self.central_force_power = central_force_power
		self.central_force = central_force
		self.collision_scaling_factor = self.size*10
		self.track = [ [] for ball in range(len(self.state))]

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
		#Gravity is applied as a force independant of particle mass. v_x = - g_x * dt, v_y = - g_y * dt.
		for n in range(0, len(self.state)):
			self.state[n][2] += -self.g[0] * dt
			self.state[n][3] += -self.g[1] * dt

		#Apply drag.
		#Use a drag force that is linearly dependant on velocity. 
		#F_drag = - drag * v
		#a_drag = - drag * v / m. Particles with higher mass are less affected by drag. 
		#v_i+1 = v_i + a_drag * dt
		for n in range(0, len(self.state)):
			a_drag_x = - self.drag * self.state[n][2] / self.m[n]
			self.state[n][2] += a_drag_x * dt
			a_drag_y = - self.drag * self.state[n][3] / self.m[n]
			self.state[n][3] += a_drag_y * dt

		#Apply a central force term, attracting particles to the origin. 
		#F_central = 1/r^n, where n is a variable central force power. 
		#r = sqrt(x**2 + y**2)
		#F_x = -F x / r
		#F_y = -F y / r
		#a_x = F_x / m
		#a_y = F_y / m
		#v_i+1_x = v_i_x + a_x * dt
		#v_i+1_y = v_i_y + a_y * dt
		def c_force(state, central_force_power, mass):
			#In: coordinates, velocity, and central force
			#Out: new velocity coordinates.
			global dt
			x = state[0]
			y = state[1]
			vx = state[2]
			vy = state[3]
			r = sqrt(x**2 + y**2)
			force = 1/(r ** central_force_power)
			fx = -force*x/r
			fy = -force*y/r
			ax = fx / mass
			ay = fy / mass
			return vx + ax*dt, vy + ay*dt
		if(self.central_force):
			for n in range(0, len(self.state)):
				self.state[n][2], self.state[n][3] = c_force(self.state[n], self.central_force_power, self.m[n])

		#Append the current position to the track
		for n in range(0, len(self.state)):
			self.track[n].append([self.state[n][0],self.state[n][1]])
			if(len(self.track[n]) > 60):
				self.track[n].pop(0)

############################### Animation ###############################

#Set up initial state
#np.random.seed(0) #Set constant seed.
#num_particles = 5
init_state = -0.5 + np.random.random((num_particles, 4)) #Randomly Generate (# of particles, # of elements (4 required))
#All particle dimension start with a position and veloicty between (-0.5, 0.5) produced by a gaussain distribution about 0. 
init_state[:, :2] *= 3.9 #Multiply the starting position of each particle by 3.9. 
init_state[:, 2:] += 1 #Multiply the starting velocity of each particle by 1. 

#Define the working box variable of ParticleBox class. 
box = ParticleBox(init_state, gravity=gravity, drag=drag, central_force=central_force, central_force_power=central_force_power)

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
particles, = ax.plot([], [], 'o', ms=box.size, markerfacecolor="blue", markeredgecolor="red")
ptrack = [[] for ball_num in range(num_particles)]
for ball_num in range(num_particles):
	ptrack[ball_num], = ax.plot([], [], 'r', ms=box.size)


# rect is the box edge
rect = plt.Rectangle(box.bounds[::2], box.bounds[1] - box.bounds[0], box.bounds[3] - box.bounds[2], edgecolor="black", linewidth=2, facecolor="none")
#Rectangle(bottom left corner coordinates, width, height, ...)
ax.add_patch(rect)

#Initialize the first frame of the animation
def init():
	global box, rect
	particles.set_data([], [])
	yield particles
	yield rect
	for ball_num in range(num_particles):
		ptrack[ball_num].set_data([], [])
		yield ptrack[ball_num]
	#rect.set_edgecolor('none')
	#return particles, rect, ptrack[0]

def animate(i):
	#Sequential animation step that the animation function uses. The iterable i is not used. 
	"""perform animation step"""
	global box, rect, dt, ax, fig
	box.step(dt) #Take one step forward in time (dt). This updates all particles in box.
	
	# update pieces of the animation
	#rect.set_edgecolor('k')
	particles.set_data(box.state[:, 0], box.state[:, 1])
	yield particles
	yield rect
	for ball_num in range(num_particles):
		ptrack[ball_num].set_data(np.array([ball[0] for ball in box.track[ball_num]]), np.array([ball[1] for ball in box.track[ball_num]]))
		yield ptrack[ball_num]

animate_plot = animation.FuncAnimation(fig, animate, frames=600, interval=10, blit=True, init_func=init)
#particles and rect are the only objects that actually get plotted. 

plt.show()