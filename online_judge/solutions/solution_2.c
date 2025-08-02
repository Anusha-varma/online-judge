#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#define MAX_SUM 10001

bool isSubsetSum(int arr[], int n, int target) {
    bool dp[MAX_SUM] = {false};
    dp[0] = true;

    for (int i = 0; i < n; i++) {
        for (int j = target; j >= arr[i]; j--) {
            dp[j] = dp[j] || dp[j - arr[i]];
        }
    }

    return dp[target];
}

int main() {
    int arr[201], n = 0, target, temp;

    while (scanf("%d", &temp) == 1) {
        arr[n++] = temp;
        if (getchar() == '\n') break;
    }

    scanf("%d", &target);

    printf(isSubsetSum(arr, n, target) ? "True\n" : "False\n");
    return 0;
}
