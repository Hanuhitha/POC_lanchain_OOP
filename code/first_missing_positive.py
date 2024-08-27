def firstMissingPositive(nums):
    n = len(nums)
    present = [False] * (n + 1)
    for num in nums:
        if 1 <= num <= n:
            present[num] = True
    for i in range(1, n + 1):
        if not present[i]:
            return i
    return n + 1