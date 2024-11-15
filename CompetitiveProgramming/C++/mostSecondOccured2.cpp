/******************************************************************************

Welcome to GDB Online.
GDB online is an online compiler and debugger tool for C, C++, Python, Java, PHP, Ruby, Perl,
C#, OCaml, VB, Swift, Pascal, Fortran, Haskell, Objective-C, Assembly, HTML, CSS, JS, SQLite, Prolog.
Code, Compile, Run and Debug online from anywhere in world.

*******************************************************************************/
#include <bits/stdc++.h>
using namespace std;
int mostSecondOccurance(vector<int> arr)
{

    unordered_map<int, int> countMap;
    int mostOccured = 0, count = 0;
    int mostSecondOccured = 0, mostSecondcount = 0;

    for (auto item : arr)
    {
        countMap[item]++;
    }

    vector<pair<int, int>> CountArr(countMap.begin(), countMap.end());

    sort(CountArr.begin(), CountArr.end(), [](pair<int, int> &a, pair<int, int> &b)
         { return a.second > b.second; }); // lamda function to sort desc

    if (CountArr.size() < 2)
    {
        return -1; // Indicating there is no second most occurrence
    }
    return CountArr[1].first;
}

int main()
{
    vector<int> arr = {1, 24, 55, 47, 2, 24, 1, 4, 1};
    int res = mostSecondOccurance(arr);
    cout << res << endl;
    return 0;
}