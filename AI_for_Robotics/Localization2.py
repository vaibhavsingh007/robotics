# The function localize takes the following arguments:
#
# colors:
#        2D list, each entry either 'R' (for red cell) or 'G' (for green cell)
#
# measurements:
#        list of measurements taken by the robot, each entry either 'R' or 'G'
#
# motions:
#        list of actions taken by the robot, each entry of the form [dy,dx],
#        where dx refers to the change in the x-direction (positive meaning
#        movement to the right) and dy refers to the change in the y-direction
#        (positive meaning movement downward). Movement is cyclic
#        NOTE: the *first* coordinate is change in y; the *second* coordinate is
#              change in x
#
# sensor_right: (recall pHit and pMiss)
#        float between 0 and 1, giving the probability that any given
#        measurement is correct; the probability that the measurement is
#        incorrect is 1-sensor_right
#
# p_move:
#        float between 0 and 1, giving the probability that any given movement
#        command takes place; the probability that the movement command fails
#        (and the robot remains still) is 1-p_move; the robot will NOT overshoot
#        its destination in this exercise
#
# The function should RETURN (not just show or print) a 2D list (of the same
# dimensions as colors) that gives the probabilities that the robot occupies
# each cell in the world.
#
# Compute the probabilities by assuming the robot initially has a uniform
# probability of being in any cell.
#
# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.
#
# Motion:
#  [0,0] - stay
#  [0,1] - right
#  [0,-1] - left
#  [1,0] - down
#  [-1,0] - up

def localize(colors,measurements,motions,sensor_right,p_move):
    # initializes p to a uniform distribution over a grid of the same dimensions as colors
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    p = [[pinit for col in range(len(colors[0]))] for row in range(len(colors))]
    
    # >>> Insert your code here <<<
    if (not len(measurements) == len(motions)):
        return "Length of measurements and motions array is not same."

    for i in range(len(measurements)):
        p = move(p, motions[i], p_move)
        sense(p, colors, measurements[i], sensor_right)
    
    return p

def sense(p, colors, measurement, p_sensor):
    col_length = len(colors[0])
    row_length = len(colors)

    for row in range(row_length):
        for col in range(col_length):
            if (colors[row][col] == measurement):
                p[row][col] = p[row][col]*p_sensor
            else:
                p[row][col] = p[row][col]*(1-p_sensor)

    normalize(p)
    return

# Based on the motion rubrics defined above
def move(p, motion, p_move):
    def update_vertical(p, step, p_move):
        col_length = len(p[0])
        row_length = len(p)

        # Remember, this is very important. Do not perform in-place updates
        #..to the P array
        q = [[0.0]*col_length for i in range(row_length)]

        for col in range(col_length):
            for row in range(row_length):
                # As per the motion rubrics, update current cell with 
                #..P(current)*p_move and P(previous)*(1-p_move)
                prev_cell = (row-step) % row_length
                q[row][col] = p[prev_cell][col]*p_move + p[row][col]*(1-p_move)
                #p[prev_cell][col] = p[prev_cell][col]*(1-p_move)
        return q

    def update_horizontal(p, step, p_move):
        col_length = len(p[0])
        row_length = len(p)

        q = [[0.0]*col_length for i in range(row_length)]

        for row in range(row_length):
            for col in range(col_length):
                # As per the motion rubrics, update P(current cell) with 
                #..P(prev cell)*p_move and P(current cell)*(1-p_move)
                prev_cell = (col-step) % col_length
                q[row][col] = p[row][prev_cell]*p_move + p[row][col]*(1-p_move)
                #p[row][prev_cell] = p[row][prev_cell]*(1-p_move)
        return q

    # Extract no. of steps (U) and direction (2D) from motion [dy,dx]
    if not motion[0] == 0:
        return update_vertical(p, motion[0], p_move)
    elif not motion[1] == 0:
        return update_horizontal(p, motion[1], p_move)
    else:
        return p

def normalize(p):
    s = 0
    col_length = len(p[0])
    row_length = len(p)

    for i in range(row_length):
        s += sum(p[i])

    for row in range(row_length):
        for col in range(col_length):
            p[row][col] /= s
    return

def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
    print '[' + ',\n '.join(rows) + ']'
    
#############################################################
# For the following test case, your output should be 
# [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
#  [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
#  [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
#  [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]]
# (within a tolerance of +/- 0.001 for each entry)

colors = [['R','G','G','R','R'],
          ['R','R','G','R','R'],
          ['R','R','G','G','R'],
          ['R','R','R','R','R']]
measurements = ['G','G','G','G','G']
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]

p = localize(colors,measurements,motions,sensor_right = .7, p_move = .8)
show(p) # displays your answer
