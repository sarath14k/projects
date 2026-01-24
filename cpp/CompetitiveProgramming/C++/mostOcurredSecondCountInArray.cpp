/******************************************************************************

Welcome to GDB Online.
GDB online is an online compiler and debugger tool for C, C++, Python, Java, PHP, Ruby, Perl,
C#, OCaml, VB, Swift, Pascal, Fortran, Haskell, Objective-C, Assembly, HTML, CSS, JS, SQLite, Prolog.
Code, Compile, Run and Debug online from anywhere in world.

*******************************************************************************/
#include <bits/stdc++.h>
using namespace std;
int mostSecondOccurance(int arr[], int size)
{

    unordered_map<int, int> countMap;
    int mostOccured = 0, count = 0;
    int mostSecondOccured = 0, mostSecondcount = 0;

    for (int item = 0; item < size; item++)
    {
        countMap[arr[item]]++;
        if (countMap[arr[item]] > count)
        {

            mostOccured = arr[item];
            count = countMap[arr[item]];
        }
    }

    for (const auto &pair : countMap)
    {
        if ((pair.second > mostSecondcount) && (pair.second < count))
        {
            mostSecondcount = pair.second;
            mostSecondOccured = pair.first;
        }
    }

    return mostSecondOccured;
}

int main()
{
    int arr[] = {1, 24, 55, 47, 2, 24, 1, 4, 1};
    int size = sizeof(arr) / sizeof(arr[0]);

    int res = mostSecondOccurance(arr, size);
    cout << res << endl;
    return 0;
}