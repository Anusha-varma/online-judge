#include <iostream>
using namespace std;

int main()
{
     int n, num=1211, digit, rev = 0;

     n = num;

     do
     {
         digit = num % 10;
         rev = (rev * 10) + digit;
         num = num / 10;
     } while (num != 0);

     cout << " The reverse of the number is: " << rev << endl;

     if (n == rev and n > 0)  // Negative numbers are not palindromic
         cout << " The number is a palindrome.";
     else
         cout << " The number is not a palindrome.";

    return 0;
}