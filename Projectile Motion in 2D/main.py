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

#Settings for 2D Projectile Motion

#Number of particles
num_particles = 10

#Gravitational Acceleration (x, y)
gravity = [0, -10]

#Velocity dependant drag constant
#Recommended less than 0.1. 
drag = 0.01

#Apply a central force? (True/False)
central_force = False

#Central force power. Choose n for F = 1/r^n. 
#Recommended less than 2. 
central_force_power = 0.5

import ProjectileMotion