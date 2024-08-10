def countRegions(grid):
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    def dfs(row, col):
        if row < 0 or row >= rows or col < 0 or col >= cols or visited[row][col] or grid[row][col] == ' ': 
            return
        visited[row][col] = True
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)

    num_regions = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '\' and not visited[i][j]:
                num_regions += 1
                dfs(i, j)
    return num_regions