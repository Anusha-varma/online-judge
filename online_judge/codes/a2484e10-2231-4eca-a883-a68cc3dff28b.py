def is_subset_sum(arr, target_sum):
    n = len(arr)
    dp = [[False] * (target_sum + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = True

    for i in range(1, n + 1):
        for j in range(1, target_sum + 1):
            if arr[i - 1] > j:
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = dp[i - 1][j] or dp[i - 1][j - arr[i - 1]]

    return dp[n][target_sum]


if __name__ == "__main__":
    try:
        arr = list(map(int, input().strip().split()))
        target_sum = int(input().strip())
        if is_subset_sum(arr, target_sum):
            print("true")
        else:
            print("false")
    except Exception as e:
        print("Error:", e)