#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int main() {
    char s[1001], p[1001];
    scanf("%s %s", s, p);
    int m = strlen(s), n = strlen(p);
    bool **dp = (bool **)malloc((m + 1) * sizeof(bool *));
    for (int i = 0; i <= m; i++)
        dp[i] = (bool *)calloc(n + 1, sizeof(bool));

    dp[0][0] = true;
    for (int j = 2; j <= n; ++j)
        if (p[j - 1] == '*')
            dp[0][j] = dp[0][j - 2];

    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (p[j - 1] == '.' || p[j - 1] == s[i - 1])
                dp[i][j] = dp[i - 1][j - 1];
            else if (p[j - 1] == '*')
                dp[i][j] = dp[i][j - 2] || ((p[j - 2] == s[i - 1] || p[j - 2] == '.') && dp[i - 1][j]);
        }
    }

    printf(dp[m][n] ? "true\n" : "false\n");

    for (int i = 0; i <= m; i++)
        free(dp[i]);
    free(dp);
    return 0;
}
