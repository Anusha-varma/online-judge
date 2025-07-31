#include <stdio.h>

int main() {
    int num, reversed = 0, remainder, original;

    scanf("%d", &num);

    original = num;
    while (num != 0) {
        remainder = num % 10;
        reversed = reversed * 10 + remainder;
        num /= 10; 
    }

    if (original == reversed) {
        printf("YES");
    } else {
        printf("NO");
    }

    return 0;
}