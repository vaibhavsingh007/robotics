# --------------
# USER INSTRUCTIONS
#
# Write a function called stochastic_value that 
# returns two grids. The first grid, value, should 
# contain the computed value of each cell as shown 
# in the video. The second grid, policy, should 
# contain the optimum policy for each cell.
#
# --------------
# GRADING NOTES
#
# We will be calling your stochastic_value function
# with several different grids and different values
# of success_prob, collision_cost, and cost_step.
# In order to be marked correct, your function must
# RETURN (it does not have to print) two grids,
# value and policy.
#
# When grading your value grid, we will compare the
# value of each cell with the true value according
# to this model. If your answer for each cell
# is sufficiently close to the correct answer
# (within 0.001), you will be marked as correct.

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

# ---------------------------------------------
#  Modify the function stochastic_value below
# ---------------------------------------------

def stochastic_value(grid,goal,cost_step,collision_cost,success_prob):
    failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
    value = [[collision_cost for col in range(len(grid[0]))] for row in range(len(grid))]
    policy = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]

    updated = True
    while updated:
        updated = False

        # We will be populating the values using the value function bottom up
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                current_min = collision_cost
                min_o = 0
                for o in range(4):
                    # If reached the goal state, assign it 0
                    if [r,c] == goal:
                        if value[r][c] != 0:
                            value[r][c] = 0
                            policy[r][c] = "*"
                            updated = True
                    elif grid[r][c] == 0:
                        adj_i = r + delta[o][0]
                        adj_j = c + delta[o][1]

                        if len(grid) > adj_i >= 0 and len(grid[0]) > adj_j >= 0 and grid[adj_i][adj_j] == 0:
                            min = success_prob*value[adj_i][adj_j]
                        else:
                            min = success_prob*collision_cost

                        # Left cell
                        left_o = (o+1)%4
                        left_i = r + delta[left_o][0]
                        left_j = c + delta[left_o][1]

                        if len(grid) > left_i >= 0 and len(grid[0]) > left_j >= 0 and grid[left_i][left_j] == 0:
                            min += failure_prob*value[left_i][left_j]
                        else:
                            min += failure_prob*collision_cost

                        # Right cell
                        right_o = (o-1)%4
                        right_i = r + delta[right_o][0]
                        right_j = c + delta[right_o][1]

                        if len(grid) > right_i >= 0 and len(grid[0]) > right_j >= 0 and grid[right_i][right_j] == 0:
                            min += failure_prob*value[right_i][right_j]
                        else:
                            min += failure_prob*collision_cost

                        min += 1    # Cost of motion

                        if min < current_min:
                            current_min = min
                            min_o = o

                # Finally, update value and policy
                if current_min < value[r][c]:
                    value[r][c] = current_min
                    policy[r][c] = delta_name[min_o]
                    updated = True
    
    return value, policy

# ---------------------------------------------
#  Use the code below to test your solution
# ---------------------------------------------

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]
goal = [0, len(grid[0])-1] # Goal is in top right corner
cost_step = 1
collision_cost = 100
success_prob = 0.5

value,policy = stochastic_value(grid,goal,cost_step,collision_cost,success_prob)
for row in value:
    print row
for row in policy:
    print row

# Expected outputs:
#
# [57.9029, 40.2784, 26.0665,  0.0000]
# [47.0547, 36.5722, 29.9937, 27.2698]
# [53.1715, 42.0228, 37.7755, 45.0916]
# [77.5858, 100.00, 100.00, 73.5458]
#
# ['>', 'v', 'v', '*']
# ['>', '>', '^', '<']
# ['>', '^', '^', '<']
# ['^', ' ', ' ', '^']
