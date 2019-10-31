"""
Physics 18L - Experiment 4 - Day 2
Christian Lee
  
Professor: N. Whitehorn
TA: Teresa Le
Lab Date: Thursday, Oct 24, 2019
UCLA Physics Department

Required libraries: matplotlib, numpy, scipy

Projectile motion in 2D
"""

#Settings for 2D Projectile Motion

#Number of particles
num_particles = 5

#Gravitational Acceleration (x, y)
gravity = [0, -1]

#Velocity dependant drag constant
#Recommended less than 0.1. 
drag = 0

#Apply a central force? (True/False)
#If true, set ball_collisions -> False
central_force = False

#Central force power. Choose n for F = 1/r^n. 
#Recommended less than 2. 
central_force_power = 0.1

#Mass of the balls. Recommended 0.05
ball_mass = 0.05

#Random mass. If true, the particles will have varrying masses based on a gaussian distribution about mass.
#If false, all particles will have uniform mass. 
#Forces affect particles of different masses differently
random_mass = False

#Ball collisions. If true, balls will bounce off of each other. 
ball_collisions = True

import ProjectileMotion