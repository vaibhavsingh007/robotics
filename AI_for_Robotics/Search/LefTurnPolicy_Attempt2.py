# ----------
# User Instructions:
# 
# Implement the function optimum_policy2D below.
#
# You are given a car in grid with initial state
# init. Your task is to compute and return the car's 
# optimal path to the position specified in goal; 
# the costs for each motion are as defined in cost.
#
# There are four motion directions: up, left, down, and right.
# Increasing the index in this array corresponds to making a
# a left turn, and decreasing the index corresponds to making a 
# right turn.

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # go right
forward_name = ['up', 'left', 'down', 'right']

# action has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

# EXAMPLE INPUTS:
# grid format:
#     0 = navigable space
#     1 = unnavigable space 
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

init = [4, 3, 0] # given in the form [row,col,direction]
                 # direction = 0: up
                 #             1: left
                 #             2: down
                 #             3: right
                
goal = [2, 0] # given in the form [row,col]

cost = [2, 1, 20] # cost has 3 values, corresponding to making 
                  # a right turn, no turn, and a left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D with the given parameters should return 
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
# ----------

# ----------------------------------------
# modify code below
# ----------------------------------------

def optimum_policy2D(grid,init,goal,cost):

    # Initialize a 3D value array [o][r][c] for DP
    rows = len(grid)
    cols = len(grid[0])
    values = [[[999]*cols for i in range(rows)] for j in range(4)]
    policy = [[[' ']*cols for i in range(rows)] for j in range(4)]
    policy2D = [[' ']*cols for i in range(rows)]

    updated = True
    while updated:
        updated = False

        # We will be populating the values using the value function bottom up
        for r in range(rows):
            for c in range(cols):
                for o in range(4):
                    # If reached the goal state, assign it 0
                    if [r,c] == goal:
                        if values[o][r][c] != 0:
                            values[o][r][c] = 0
                            policy[o][r][c] = "*"
                            updated = True
                    elif grid[r][c] == 0:
                        # Propagate best value for reaching from current cell to
                        #..the next by applying all possible actions in the current orientation.
                        for a in range(len(action)):
                            new_o = (o + action[a]) % 4     # It's cyclic
                            adj_r = r + forward[new_o][0]
                            adj_c = c + forward[new_o][1]

                            # Check bounds and if navigable
                            if len(grid) > adj_r >= 0 and len(grid[0]) > adj_c >= 0 and grid[adj_r][adj_c] == 0:
                                # So, the value from the current cell to current adjacent depending on
                                #..the new orientation, as a result of applying the current action is
                                new_val = values[new_o][adj_r][adj_c] + cost[a]

                                if new_val < values[o][r][c]:
                                    values[o][r][c] = new_val
                                    policy[o][r][c] = a
                                    updated = True
    #for i in range(len(policy)):
    #    for j in range(len(policy[i])):
    #        print policy[i][j]
    #    print
    #print
    #print

    #for i in range(len(policy)):
    #    for j in range(len(policy[i])):
    #        print values[i][j]
    #    print
    #print
    #print
            

    # Now is the time to populate the policy in 2D
    i = init[0]
    j = init[1]
    current_o = init[2]
    
    while [i,j] != goal:    #TODO: Add more conditions
        optimal_action = policy[current_o][i][j]
        policy2D[i][j] = action_name[optimal_action]

        # Take the optimal_o
        current_o = (current_o + action[optimal_action]) % 4
        i = i + forward[current_o][0]
        j = j + forward[current_o][1]
    policy2D[i][j] = "*"

    return policy2D

res = optimum_policy2D(grid, init, goal, cost)
for i in range(len(res)):
    print res[i]
