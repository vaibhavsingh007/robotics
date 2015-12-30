# In this exercise, you should implement the
# resampler shown in the previous video.

from math import *
import random
from MovingRobot import robot

landmarks  = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]]
world_size = 100.0

# Resamples particles
def resample(weights, n):
    beta = 0
    max_w = max(weights)*2
    current_item = random.randint(0,n-1)
    result = []
    
    for i in range(n):
        beta += random.uniform(0,max_w)
        
        # Remember the pie chart (disc) model?
        while weights[current_item] < beta:
            beta -= weights[current_item]
            current_item = (current_item + 1) % n
        else:
            result.append(current_item)
    return result

####   DON'T MODIFY ANYTHING ABOVE HERE! ENTER CODE BELOW ####
myrobot = robot()
myrobot = myrobot.move(0.1, 5.0)    # Original robot moves
Z = myrobot.sense()

N = 1000
p = []

# Generate N random particles
for i in range(N):
    x = robot()
    x.set_noise(0.05, 0.05, 5.0)
    p.append(x)

# Simulate original robot motion on each particle
p2 = []
for i in range(N):
    p2.append(p[i].move(0.1, 5.0))
p = p2

# Update the prob. of every single particle being closest to the original robot
w = []
for i in range(N):
    w.append(p[i].measurement_prob(Z))

# Normalize all weights
normalizer = sum(w)

if (normalizer != 1):
    for i in range(len(w)):
        w[i] /= normalizer

p3 = []
for i in resample(w, N):
    p3.append(p[i])

p = p3
print p #please leave this print statement here for grading!

