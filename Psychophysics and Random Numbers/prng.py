import random
from matplotlib import pyplot
from math import sqrt

seed = random.randrange(1, 2**32)

def lcg():
	#Linear Congruential Generator
	#V_(j+1) = ( V_j * A + B ) mod M
	#A is the multiplier
	a = 1664525
	#B is the increment
	b = 1013904223
	#M is the modulus
	m = 2**32
	#V_j is the seed
	#Function returns a float in [0, 1)

	global seed #Allow lcg to modify seed

	seed = ((seed * a) + b) % m 
	return seed / 2**32

def verify_uniform_hist():
	rand = []
	for i in range(0,10000):
		rand.append(lcg())

	pyplot.hist(rand, bins = 100)
	pyplot.show()
#Uncomment below to produce a histogram of 10000 points generated from the lcg function. It should create a uniform histogram showing that lcg is uniformly distributed. 
#verify_uniform_hist()

def ring(rad_a = 10, rad_b = 12, n=20):
	#Generate a random point that falls within a ring of inner radius rad_a and outer radius rad_b
	#Assume rad_a < rad_b

	if rad_a == rad_b:
		raise ValueError("The ring has width zero.")

	if rad_a > rad_b:
		rad_a, rad_b = rad_b, rad_a

	x = []
	y = []

	while(len(x) < n):
		rand_x = random.uniform(0, rad_b) * random.randrange(-1, 2, 2) #Generate a random number in (-rad_b, rad_b)
		rand_y = random.uniform(0, rad_b) * random.randrange(-1, 2, 2) #Generate a random number in (-rad_b, rad_b)
		if rad_a <= sqrt(rand_x**2 + rand_y**2) <= rad_b: 
			#Test to see if the point falls within the ring. I
			x.append(rand_x)
			y.append(rand_y)
	
	#Plot spaghetti
	pyplot.ion()
	circlea = pyplot.Circle((0, 0), rad_a, fill=False, color = "blue")
	circleb = pyplot.Circle((0,0), rad_b, fill=False, color = "blue")
	fig, ax = pyplot.subplots() 
	ax.add_artist(circlea)
	ax.add_artist(circleb)
	ax.set(xlim=(-rad_b, rad_b), ylim=(-rad_b, rad_b))
	pyplot.plot(x, y, "ro")
	pyplot.draw()
	pyplot.pause(0.0001)
	pyplot.clf()
	
#Plot 30 figures.
for i in range(0,30):
	ring()