# ----------
import copy
# User Instructions:
# 
# Create a function compute_value which returns
# a grid of values. The value of a cell is the minimum
# number of moves required to get from the cell to the goal. 
#
# If a cell is a wall or it is impossible to reach the goal from a cell,
# assign that cell a value of 99.
# ----------

grid = [[0, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0]]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1 # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

def compute_value(grid,goal,cost):
    # ----------------------------------------
    # insert code below
    # ----------------------------------------
    a = [[" "]*len(grid[0]) for i in range(len(grid))]
    #obstacles = []  # Optimization for replacing -1s with 99, later.

    # Invoke search from every possible cell
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 0: # Navigable?
                grid_copy = copy.deepcopy(grid)
                search(grid_copy, [row,col], goal, cost, a)
            #else:
            #    obstacles.append([row,col])

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if a[row][col] == -1:
                a[row][col] = 99
    
    # make sure your function returns a grid of values as 
    # demonstrated in the previous lecture.
    return a 

def search(grid,init,goal,cost,cache):

    # TODO: Create the heuristic function (for now, just sneaking this in)
    heuristic = [[9, 8, 7, 6, 5, 4],
                [8, 7, 6, 5, 4, 3],
                [7, 6, 5, 4, 3, 2],
                [6, 5, 4, 3, 2, 1],
                [5, 4, 3, 2, 1, 0]]

    element_parent = {} # Convention: {[expanded cell]:[[parent],[parent's expansion symbol for this cell]]}

    ################################
    q = []  # For BFS # Format --> [f,g,i,j]: f=g+h, g=cost, i/j=indices (cell)
    i = init[0]
    j = init[1]

    # Dynamic Programming cache check
    if cache[i][j] != " ":
        return

    grid[i][j] = -1   # Mark explored
    q.append([heuristic[i][j],0,i,j])
    #q.append([0,i,j])
    element_parent["%s_%s" % (i,j)] = parent([],"") # Insert root
    
    c = 0   # Cost counter

    while len(q) > 0:
        current = q.pop(0)
        c = current[1]
        i = current[2]      # Current cell's indices
        j = current[3]

        # Dynamic Programming cache check OR goal
        if cache[i][j] != " " or [i,j] == goal:
            if [i,j] == goal:
                cache[i][j] = "*"
            populate_values(cache, element_parent, "%s_%s" % (i,j))
            return

        # Add (unexplored) adjacents to the queue
        # Add adjacent to pending if navigable (=0)
        for k in range(len(delta)):
            adj_i = i + delta[k][0]
            adj_j = j + delta[k][1]

            if len(grid) > adj_i >= 0 and len(grid[0]) > adj_j >= 0 and grid[adj_i][adj_j] == 0:
                grid[adj_i][adj_j] = -1     # Mark explored
                
                # Heuristic plumbing
                g = c + cost
                h = heuristic[adj_i][adj_j]
                f = g + h   # To be used only to sort the q
                q.append([f, g, adj_i, adj_j])
                q = sorted(q)   # Simulating min heap on 'f'

                element_parent["%s_%s" % (adj_i,adj_j)] = parent([i,j], delta_name[k])

    return "fail"

def populate_values(a, dict, current):
    parent = dict[current]   # current element's parent and navigation symbol

    while parent.is_valid:    # eventually must reach the root
        # Mark symbol on 'a' 2D array
        a[parent.indices[0]][parent.indices[1]] = parent.symbol
        parent = dict[parent.to_str()]
        valid = parent.is_valid
    return

class parent():
    def __init__(self, indices, symbol):
        self.indices = indices
        self.symbol = symbol
        self.is_valid = (len(self.indices) > 0)

    def to_str(self):
        return "%s_%s" % (self.indices[0], self.indices[1])

res = compute_value(grid, goal, cost)
for i in range(len(res)):
    print res[i]
        