#include <iostream>
#include <string>
using namespace std;

string longestPalindrome(string s) {
    int start = 0, maxLen = 0;
    for (int i = 0; i < s.length(); i++) {
        for (int a = i, b = i; b < s.length() && a >= 0 && s[a] == s[b]; a--, b++) {
            if (b - a + 1 > maxLen) {
                start = a;
                maxLen = b - a + 1;
            }
        }
        for (int a = i, b = i + 1; b < s.length() && a >= 0 && s[a] == s[b]; a--, b++) {
            if (b - a + 1 > maxLen) {
                start = a;
                maxLen = b - a + 1;
            }
        }
    }
    return s.substr(start, maxLen);
}

int main() {
    string s;
    cin >> s;
    cout << longestPalindrome(s) << endl;
    return 0;
}
