from PController import robot
from math import pi

# Implement a PD controller by running 100 iterations
# of robot motion. The steering angle should be set
# by the parameter tau so that:
#
# steering = -tau_p * CTE - tau_d * diff_CTE
# where differential crosstrack error (diff_CTE)
# is given by CTE(t) - CTE(t-1)
# assuming delta(t) = 1

# ------------------------------------------------------------------------
#
# run - does a single control run.


def run(param1, param2):
    myrobot = robot()
    myrobot.set(0.0, 1.0, 0.0)
    speed = 1.0 # motion distance is equal to speed (we assume time = 1)
    N = 100
    prev_cte = myrobot.y
    
    for i in range(N):
        current_cte = myrobot.y     # Reference trajectory = x axis (y=0)
        steer = -param1*current_cte - param2*(current_cte - prev_cte)
        prev_cte = current_cte
        myrobot = myrobot.move(steer, speed)
        print myrobot, steer

# Call your function with parameters of 0.2 and 3.0 and print results
run(0.2, 3.0)