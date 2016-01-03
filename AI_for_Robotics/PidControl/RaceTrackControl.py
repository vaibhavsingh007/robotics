# --------------
# User Instructions
# 
# Define a function cte in the robot class that will
# compute the crosstrack error for a robot on a
# racetrack with a shape as described in the video.
#
# You will need to base your error calculation on
# the robot's location on the track. Remember that 
# the robot will be traveling to the right on the
# upper straight segment and to the left on the lower
# straight segment.
#
# --------------
# Grading Notes
#
# We will be testing your cte function directly by
# calling it with different robot locations and making
# sure that it returns the correct crosstrack error.  
 
from math import *
import random
from PController import robot
    
def cte(self, radius):
        left_centre = [radius,radius]
        right_centre = [3*radius,radius]
        cte = 0

        # if robot's x,y are more than r,r, then robot is on the upper half
        if left_centre[0] <= self.x < right_centre[0]:
            if self.y > left_centre[0]:
                cte = self.y - 2*radius
            else:
                cte = -self.y   # Caveat: invert sign as robot moving left
        elif right_centre[0] <= self.x:
            # Find Euclidean distance to right-centre
            d = sqrt((self.x - right_centre[0])**2 + (self.y - right_centre[1])**2)
            cte = d - radius
        elif self.x < left_centre[0]:
            d = sqrt((self.x - left_centre[0])**2 + (self.y - left_centre[1])**2)
            cte = d - radius

        return cte

robot.cte = cte

# ------------------------------------------------------------------------
#
# run - does a single control run.


def run(params, radius, printflag = False):
    myrobot = robot()
    myrobot.set(0.0, radius, pi / 2.0)
    speed = 1.0 # motion distance is equal to speed (we assume time = 1)
    err = 0.0
    int_crosstrack_error = 0.0
    N = 200

    crosstrack_error = myrobot.cte(radius) # You need to define the cte function!

    for i in range(N*2):
        diff_crosstrack_error = - crosstrack_error
        crosstrack_error = myrobot.cte(radius)
        diff_crosstrack_error += crosstrack_error
        int_crosstrack_error += crosstrack_error
        steer = - params[0] * crosstrack_error \
                - params[1] * diff_crosstrack_error \
                - params[2] * int_crosstrack_error
        myrobot = myrobot.move(steer, speed)
        if i >= N:
            err += crosstrack_error ** 2
        if printflag:
            print myrobot
    return err / float(N)

radius = 25.0
params = [10.0, 15.0, 0]
err = run(params, radius, True)
print '\nFinal parameters: ', params, '\n ->', err
