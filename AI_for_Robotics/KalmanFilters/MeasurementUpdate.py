# Write a program to update your mean and variance
# when given the mean and variance of your belief
# and the mean and variance of your measurement.
# This program will update the parameters of your
# belief function. This program implements a 1-D
# Kalman Filter.

def update(mean1, var1, mean2, var2):
    new_mean = (mean1*var2 + mean2*var1)/(var1 + var2)
    new_var = 1/(1/var1 + 1/var2)
    return [new_mean, new_var]

print update(10.,8.,13., 2.)
# Output: [12.4, 1.6]

# Motion update is relatively easier, in that, the
#..Gaussians are simply added.
def predict(mean1, var1, mean2, var2):
    new_mean = mean1 + mean2
    new_var = var1 + var2
    return [new_mean, new_var]

print predict(10., 4., 12., 4.)
# Output: [22.0, 8.0]

# Using a more complex scenario (i/p)
measurements = [5., 6., 7., 9., 10.]
motion = [1., 1., 2., 1., 1.]
measurement_sig = 4.
motion_sig = 2.
mu = 0.
sig = 10000.

#Please print out ONLY the final values of the mean
#and the variance in a list [mu, sig]. 

# Insert code here
for i in range(len(measurements)):
    updated = update(mu, sig, measurements[i], measurement_sig)
    mu = updated[0]
    sig = updated[1]    # Note this caveat. Measurements and motion variances
                        #..are not updated. Only the original variance is.
    #measurement_sig = updated[1]
    updated = predict(mu, sig, motion[i], motion_sig)
    mu = updated[0]
    sig = updated[1]
    #motion_sig = updated[1]

print [mu, sig]