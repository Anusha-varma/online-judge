#include <stdio.h>
#include <string.h>

int expandCenter(char *s, int left, int right) {
    while (left >= 0 && right < strlen(s) && s[left] == s[right]) {
        left--;
        right++;
    }
    return right - left - 1;
}

int main() {
    char s[1001], res[1001];
    scanf("%s", s);
    int start = 0, maxLen = 0;

    for (int i = 0; i < strlen(s); i++) {
        int len1 = expandCenter(s, i, i);
        int len2 = expandCenter(s, i, i + 1);
        int len = len1 > len2 ? len1 : len2;
        if (len > maxLen) {
            maxLen = len;
            start = i - (len - 1) / 2;
        }
    }

    strncpy(res, s + start, maxLen);
    res[maxLen] = '\0';
    printf("%s\n", res);
    return 0;
}
