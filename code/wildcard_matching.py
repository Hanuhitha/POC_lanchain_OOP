def isMatch(s, p):
    if len(p) == 0: return len(s) == 0
    dp = [[False for _ in range(len(p) + 1)] for _ in range(len(s) + 1)]
    dp[0][0] = True
    for index in range(1, len(dp[0])):
        if p[index - 1] == '*':
            dp[0][index] = dp[0][index - 1]
    for i in range(1, len(dp)):
        for j in range(1, len(dp[0])):
            if s[i - 1] == p[j - 1] or p[j - 1] == '?':
                dp[i][j] = dp[i - 1][j - 1]
            elif p[j - 1] == '*':
                dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
            else:
                dp[i][j] = False
    return dp[len(s)][len(p)]