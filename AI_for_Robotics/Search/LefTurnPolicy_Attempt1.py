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

''' FAILED: Attempted to solve without using DP. This prob. requires DP '''
def optimum_policy2D(grid,init,goal,cost):

    # Including plumbing for displaying navigation path gimmick
    a = [[" "]*len(grid[0]) for i in range(len(grid))]
    element_parent = {} # Convention: {[expanded cell]:parent()}

    ################################
    q = []  # For BFS
    i = init[0]
    j = init[1]
    o = init[2] # Orientation
    q.append([0,i,j,o])
    grid[i][j] = -1   # Mark explored
    element_parent["%s_%s" % (i,j)] = parent([], 0, 0) # insert root
    # Insert init's parent
    c = 0   # Cost counter

    goal_found = False

    while len(q) > 0:
        current = q.pop(0)
        c = current[0]      # Current cell's cost
        i = current[1]      # Current cell's indices
        j = current[2]
        o = current[3]      # Current cell's orientation (check 'action' array)

        # Check for goal
        if [i,j] == goal:
            print "Success"
            goal_found = True

        # To be used to prevent selecting its own parent from
        #..adjacent cells
        current_parent = element_parent["%s_%s" % (i,j)]

        # Add (unexplored) adjacent cells to the queue
        for k in range(len(forward)):
            adj_i = i + forward[k][0]
            adj_j = j + forward[k][1]
            
            if len(grid) > adj_i >= 0 and \
                len(grid[0]) > adj_j >= 0 and \
                grid[adj_i][adj_j] != 1 and \
                [adj_i,adj_j] != current_parent.indices:   # Avoid going back
                    # Current adjacent cell's cost
                    adj_cost = c + get_turning_cost(o, k)
                    parent_obj = parent([i,j], k, c, adj_cost)

                    if grid[adj_i][adj_j] == -1:    # Already explored?
                        # Find the last cost from its parent obj
                        prev_cost = 0
                        # Its parent must be present
                        prev_cost = element_parent["%s_%s" % (adj_i,adj_j)].childs_cost
                        
                            
                        if adj_cost < prev_cost:
                            # Add to queue with new (and better) cost and update parent
                            q.append([adj_cost, adj_i, adj_j, k])
                            q = sorted(q)
                            element_parent["%s_%s" % (adj_i,adj_j)] = parent_obj
                    else:
                        grid[adj_i][adj_j] = -1     # Mark explored
                        q.append([adj_cost, adj_i, adj_j, k])
                        q = sorted(q)
                        element_parent["%s_%s" % (adj_i,adj_j)] = parent_obj
    
    if goal_found:
        i = goal[0]
        j = goal[1]
        a[i][j] = "*"
        print_path(a, element_parent, "%s_%s" % (i,j))
        return a
    
    return "fail"

# Takes current orientation and navigation (simply, index of the 'forward' array)
#..and returns the cost of the current cell
def get_turning_cost(orientation, nav):
    c = 0   # cost

    up = 0      # Populating variables using rubrics given above.
    left = 1
    down = 2
    right = 3
    right_turn = 0
    left_turn = 2
    no_turn = 1

    if orientation == up:     # Parent's direction was 'up'
        if nav == right:
            c = cost[right_turn]
        elif nav == down:
            # Turning back is not allowed
            pass
        elif nav == left:
            c = cost[left_turn]
        elif nav == up:
            c = cost[no_turn]
    elif orientation == left:
        if nav == right:        
            # Turning back is not allowed
            pass
        elif nav == down:
            c = cost[left_turn]
        elif nav == left:
            c = cost[no_turn]
        elif nav == up:
            c = cost[right_turn]
    elif orientation == down:
        if nav == right:
            c = cost[left_turn]    
        elif nav == down:
            c = cost[no_turn]
        elif nav == left:
            c = cost[right_turn]
        elif nav == up:
            # Turning back is not allowed
            pass
    elif orientation == right:
        if nav == right:
            c = cost[no_turn]
        elif nav == down:
            c = cost[right_turn]
        elif nav == left:
            # Turning back is not allowed
            pass
        elif nav == up:
            c = cost[left_turn]

    return c



def print_path(a, dict, current):
    parent = dict[current]   # current element's parent and navigation symbol

    while parent.is_valid:    # eventually must reach the root
        # Mark symbol on 'a' 2D array
        a[parent.indices[0]][parent.indices[1]] = parent.symbol
        parent = dict[parent.to_str()]
        valid = parent.is_valid

class parent():
    def __init__(self, indices, symbol, cost, child_cost=0):
        self.indices = indices
        self.symbol = symbol    # Represents direction that lead to the child
        self.cost = cost
        self.childs_cost = child_cost   # Book-keeping: Cost of this parent's child
        self.is_valid = (len(self.indices) > 0)

    def to_str(self):
        return "%s_%s" % (self.indices[0], self.indices[1])

res = optimum_policy2D(grid, init, goal, cost)
for i in range(len(res)):
    print ".".join(res[i])


def optimum_policy2D(grid,init,goal,cost):
    
    value = [[[999for col in range(len(grid[0]))] for row in range(len(grid))],[[999for col in range(len(grid[0]))] for row in range(len(grid))],[[999for col in range(len(grid[0]))] for row in range(len(grid))],[[999for col in range(len(grid[0]))] for row in range(len(grid))]]
    print value
    queue = []
    
    x = init[1]
    y = init[0]
    dir = init[2]
    val = 0
    
    value[dir][x][y] = val
    
    queue.append([val, y, x, dir])
    
    while len(queue) != 0:
        queue.sort()
        queue.reverse()
        next = queue.pop()
        
        val = next[0]
        y = next[1]
        x = next[2]
        dir = next[3]
        
        #print "next is y: {} x: {} dir: {} val {}".format(y,x,dir,val)
        
        for i in range(len(action)):
            dir2 = (dir + action[i]) % 4 
            y2 = y + forward[dir2][0]
            x2 = x + forward[dir2][1]
            val2 = val + cost[i]
            
            #print "try y: {} x: {} dir: {} val {}".format(y2,x2,dir2,val2)
            
            
            if x2 < len(grid[0]) and x2 >= 0 and y2 < len(grid) and y2 >= 0:
                #print "in bounds"
                if value[dir2][y2][x2] > val2 and grid[y2][x2] == 0:
                    
                    #print "accepted"
                    
                    queue.append([val2, y2, x2, dir2])
                    value[dir2][y2][x2] = val2
        #print "----"
    
    
    # finding values works!!!
    
    x = goal[1]
    y = goal[0]
    
    dir = 0
    
    for i in range(3):
        if value[i+1][x][y] < value[dir][x][y]:
            dir = i + 1
            
    val = value[dir][x][y]
    
    goalBool = False
            
    policy2D = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))] 
    
    policy2D[x][y] = '*'
        
    while not goalBool:
        if y == init[0] and x == init[1]:
            goalBool = True
        else:
            
            #print "this y: {} x: {} dir: {}".format(y,x, forward_name[dir])
            
            x2 = x - forward[dir][1]
            y2 = y - forward[dir][0]
            
            #print "last y: {} x: {}".format(y2,x2)
            
            for i in range(len(action)):

                dir2 = (dir - action[i]) % 4
                
                #print "try dir {}".format(forward_name[dir2])
                
                if value[dir][x][y] - cost[i] == value[dir2][y2][x2]:
                    
                    #print "accepted"
                    
                    y = y2
                    x = x2
                    dir = dir2
                    policy2D[x][y] = action_name[i]
                    break
    
    
    
    return policy2D