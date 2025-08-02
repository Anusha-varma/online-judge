def isSubsetSum(arr, target):
    dp = [False] * (target + 1)
    dp[0] = True
    for num in arr:
        for j in range(target, num - 1, -1):
            dp[j] = dp[j] or dp[j - num]
    return dp[target]

arr = list(map(int, input().split()))
target = int(input())
print("True" if isSubsetSum(arr, target) else "False")
