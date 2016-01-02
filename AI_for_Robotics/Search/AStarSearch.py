# -----------
# User Instructions:
#
# Modify the the search function so that it becomes
# an A* search algorithm as defined in the previous
# lectures.
#
# Your function should return the expanded grid
# which shows, for each element, the count when
# it was expanded or -1 if the element was never expanded.
# 
# If there is no path from init to goal,
# the function should return the string 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]]
heuristic = [[9, 8, 7, 6, 5, 4],
             [8, 7, 6, 5, 4, 3],
             [7, 6, 5, 4, 3, 2],
             [6, 5, 4, 3, 2, 1],
             [5, 4, 3, 2, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

delta_name = ['^', '<', 'v', '>']

def search(grid,init,goal,cost):
    a = [[-1]*len(grid[0]) for i in range(len(grid))]

    ################################
    q = []  # For BFS
    # Format --> [f,g,i,j]: f=g+h, g=cost, i/j=indices (cell)
    i = init[0]
    j = init[1]
    grid[i][j] = -1   # Mark explored

    q.append([heuristic[i][j],0,i,j])
    c = 0   # Cost counter

    count = 0   # Navigation counter
    

    while len(q) > 0:
        current = q.pop(0)
        c = current[1]      # Current 'g' function (or simply put, cost)
        i = current[2]      # Current cell's indices
        j = current[3]
        a[i][j] = count
        count += 1

        # Check for goal
        if [i,j] == goal:
            print "Success"
            print [c, i, j]
            print
            return a

        # Add (unexplored) adjacents to the queue
        # Add adjacent to pending if navigable (=0)
        for d in delta:
            adj_i = i + d[0]
            adj_j = j + d[1]

            if len(grid) > adj_i >= 0 and len(grid[0]) > adj_j >= 0 and grid[adj_i][adj_j] == 0:
                grid[adj_i][adj_j] = -1     # Mark explored

                # Heuristic plumbing
                g = c + cost
                h = heuristic[adj_i][adj_j]
                f = g + h   # To be used only to sort the q
                q.append([f, g, adj_i, adj_j])
                q = sorted(q)   # Simulating min heap on 'f'

    return "fail"

res = search(grid, init, goal, cost)
for i in range(len(res)):
    print res[i]