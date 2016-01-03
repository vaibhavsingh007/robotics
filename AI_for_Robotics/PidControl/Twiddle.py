# ----------------
# User Instructions
#
# Implement twiddle as shown in the previous two videos.
# Your accumulated error should be very small!
#
# Your twiddle function should RETURN the accumulated
# error. Try adjusting the parameters p and dp to make
# this error as small as possible.
#
# Try to get your error below 1.0e-10 with as few iterations
# as possible (too many iterations will cause a timeout).
# No cheating!
# ------------
 
from math import *
import random
from PController import robot


# ------------------------------------------------------------------------
#
# run - does a single control run.


def run(params, printflag = False):
    myrobot = robot()
    myrobot.set(0.0, 1.0, 0.0)
    speed = 1.0
    err = 0.0
    int_crosstrack_error = 0.0
    N = 100
    # myrobot.set_noise(0.1, 0.0)
    myrobot.set_steering_drift(10.0 / 180.0 * pi) # 10 degree steering error


    crosstrack_error = myrobot.y


    for i in range(N * 2):

        diff_crosstrack_error = myrobot.y - crosstrack_error
        crosstrack_error = myrobot.y
        int_crosstrack_error += crosstrack_error

        steer = - params[0] * crosstrack_error  \
            - params[1] * diff_crosstrack_error \
            - int_crosstrack_error * params[2]
        myrobot = myrobot.move(steer, speed)
        if i >= N:
            err += (crosstrack_error ** 2)
        if printflag:
            print myrobot, steer
    return err / float(N)

# Coordinated Ascent
def twiddle(tol = 0.2): #Make this tolerance bigger if you are timing out!
    
    p = [0,0,0]
    dp = [1,1,1]

    best_err = run(p)

    while sum(dp) > tol:
        for i in range(len(p)):
            p[i] += dp[i]   # Increase param by probe interval
            err = run(p)

            if err < best_err:
                # Increase this probe interval to see if this further improves (reduces) our error
                dp[i] *= 1.1
                best_err = err
            else:
                # Shift p in the other direction
                p[i] -= 2*dp[i]

                # Repeat error check
                err = run(p)

                if err < best_err:
                    # Increase this probe interval to see if this further improves (reduces) our error
                    dp[i] *= 1.1
                    best_err = err
                else:
                    # Set p[i] back to the original value (little subtle) and decrease dp
                    p[i] += dp[i]
                    dp[i] *= .9
    
    return run(p)


print twiddle()
