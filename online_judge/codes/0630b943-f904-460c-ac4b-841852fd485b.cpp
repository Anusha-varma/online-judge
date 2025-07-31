#include <iostream>

int main() {
    int num, reversedNum = 0, remainder, originalNum;
    std::cin >> num;

    originalNum = num;
    while (num != 0) {
        remainder = num % 2;  
        reversedNum = reversedNum * 10 + remainder; 
        num /= 10;    
    }

    if (originalNum == reversedNum) {
        std::cout <<"YES";
    } else {
        std::cout <<"NO";
    }

    return 0;
}