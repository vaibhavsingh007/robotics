# A BFS style shortest path search

# ----------
# User Instructions:
# 
# Define a function, search() that returns a list
# in the form of [optimal path length, row, col]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

delta_name = ['^', '<', 'v', '>']

def search(grid,init,goal,cost):

    ################################
    q = []  # For BFS
    q.append([0,init[0],init[1]])
    grid[init[0]][init[1]] = -1   # Mark explored
    c = 0   # Cost counter

    while len(q) > 0:
        current = q.pop(0)
        c = current[0]
        i = current[1]      # Current cell's indices
        j = current[2]

        # Check for goal
        if [i,j] == goal:
            print "Success"
            return [c, i, j]

        # Add (unexplored) adjacents to the queue
        # Add adjacent to pending if navigable (=0)
        for d in delta:
            adj_i = i + d[0]
            adj_j = j + d[1]

            if len(grid) > adj_i >= 0 and len(grid[0]) > adj_j >= 0 and grid[adj_i][adj_j] == 0:
                grid[adj_i][adj_j] = -1     # Mark explored
                q.append([c + cost, adj_i, adj_j])

    return "fail"

print search(grid, init, goal, cost)