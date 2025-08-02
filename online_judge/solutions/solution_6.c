#include <stdio.h>
#include <stdlib.h>

#define MAXN 100005

int conflict[MAXN][20], conflict_count[MAXN];
int last_seen[MAXN];

int min(int a, int b) {
    return a < b ? a : b;
}

int count_valid(int n, int m, int cp[][2], int skip) {
    for (int i = 0; i <= n; ++i) {
        conflict_count[i] = 0;
        last_seen[i] = -1;
    }

    for (int i = 0; i < m; ++i) {
        if (i == skip) continue;
        int a = cp[i][0], b = cp[i][1];
        conflict[a][conflict_count[a]++] = b;
        conflict[b][conflict_count[b]++] = a;
    }

    int total = 0;
    int j = 0;
    for (int i = 1; i <= n; ++i) {
        while (j < n) {
            int valid = 1;
            int x = j + 1;
            for (int k = 0; k < conflict_count[x]; ++k) {
                if (last_seen[conflict[x][k]] >= i) {
                    valid = 0;
                    break;
                }
            }
            if (!valid) break;
            last_seen[x] = j + 1;
            j++;
        }
        total += (j - i + 1);
        if (last_seen[i] == i) last_seen[i] = -1;
    }

    return total;
}

int main() {
    int n, m;
    scanf("%d", &n);
    scanf("%d", &m);
    int cp[m][2];
    for (int i = 0; i < m; ++i)
        scanf("%d %d", &cp[i][0], &cp[i][1]);

    int max_sub = 0;
    for (int i = 0; i < m; ++i) {
        int res = count_valid(n, m, cp, i);
        if (res > max_sub) max_sub = res;
    }
    printf("%d\n", max_sub);
    return 0;
}
