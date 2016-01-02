# This one is another version of the Search program
#..with the display gimmicks. 

# -----------
# User Instructions:
#
# Modify the the search function so that it returns
# a shortest path as follows:
# 
# [['>', 'v', ' ', ' ', ' ', ' '],
#  [' ', '>', '>', '>', '>', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', '*']]
#
# Where '>', '<', '^', and 'v' refer to right, left, 
# up, and down motions. Note that the 'v' should be 
# lowercase. '*' should mark the goal cell.
#
# You may assume that all test cases for this function
# will have a path from init to goal.
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

delta_name = ['^', '<', 'v', '>']

def search(grid,init,goal,cost):

    # Including plumbing for displaying navigation path gimmick
    a = [[" "]*len(grid[0]) for i in range(len(grid))]
    element_parent = {} # Convention: {[expanded cell]:[[parent],[parent's expansion symbol for this cell]]}

    ################################
    q = []  # For BFS
    q.append([0,init[0],init[1]])
    grid[init[0]][init[1]] = -1   # Mark explored
    element_parent["%s_%s" % (init[0],init[1])] = parent([],"") # insert root
    # Insert init's parent
    c = 0   # Cost counter

    while len(q) > 0:
        current = q.pop(0)
        c = current[0]
        i = current[1]      # Current cell's indices
        j = current[2]

        # Check for goal
        if [i,j] == goal:
            print "Success"
            a[i][j] = "*"
            print_path(a, element_parent, "%s_%s" % (i,j))
            return a

        # Add (unexplored) adjacents to the queue
        # Add adjacent to pending if navigable (=0)
        for k in range(len(delta)):
            adj_i = i + delta[k][0]
            adj_j = j + delta[k][1]

            if len(grid) > adj_i >= 0 and len(grid[0]) > adj_j >= 0 and grid[adj_i][adj_j] == 0:
                grid[adj_i][adj_j] = -1     # Mark explored
                q.append([c + cost, adj_i, adj_j])

                element_parent["%s_%s" % (adj_i,adj_j)] = parent([i,j], delta_name[k])

    return "fail"

def print_path(a, dict, current):
    parent = dict[current]   # current element's parent and navigation symbol

    while parent.is_valid:    # eventually must reach the root
        # Mark symbol on 'a' 2D array
        a[parent.indices[0]][parent.indices[1]] = parent.symbol
        parent = dict[parent.to_str()]
        valid = parent.is_valid

class parent():
    def __init__(self, indices, symbol):
        self.indices = indices
        self.symbol = symbol
        self.is_valid = (len(self.indices) > 0)

    def to_str(self):
        return "%s_%s" % (self.indices[0], self.indices[1])

res = search(grid, init, goal, cost)
for i in range(len(res)):
    print ".".join(res[i])
