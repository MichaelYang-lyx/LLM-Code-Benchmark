
from heapq import heappop, heappush

def minPath(grid, k):
    n = len(grid)
    visited = set()
    heap = [(grid[0][0], 0, 0, [(0, 0)])]

    while heap:
        val, x, y, path = heappop(heap)
        if len(path) == k:
            return [grid[x][y] for x, y in path]

        visited.add((x, y))

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in visited:
                heappush(heap, (grid[nx][ny], nx, ny, path + [(nx, ny)]))
