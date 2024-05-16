
def minPath(grid, k):
    # Prepare the constants and variables
    N = len(grid) 
    visits = set() 
    directions = [(0, -1), (0, 1), (1, 0), (-1, 0)] 
    min_path = [N*N+1]*k 

    # we traverse through each cell in the grid. 
    # Depth-first search represented through the function DFS
    def DFS(i, j, path):
        nonlocal min_path
        
        # We add the value of the current cell to the path
        path.append(grid[i][j])
        
        # If the current path length is greater than k, we end the recursion 
        # and compare if the this path is smaller than min_path 
        if len(path)==k:
            min_path = min(min_path, path)
        else: 
            # mark this cell as visited
            visits.add((i, j))
            # And go to the neighbors
            for dx, dy in directions:
                ni, nj = i+dx, j+dy
                if 0 <= ni < N and 0 <= nj < N and (ni, nj) not in visits:
                    DFS(ni, nj, path)
                    
            # Done visiting this cell, remove it from visited cells
            visits.remove((i, j))
        
        # Remove this cell from the current path before going back to the parent call
        path.pop()
        
    # invoke the DFS from each cell in the grid    
    for i in range(N):
        for j in range(N):
            DFS(i, j, [])
            
    return min_path
