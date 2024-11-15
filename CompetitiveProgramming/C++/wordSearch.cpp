/******************************************************************************

Welcome to GDB Online.
GDB online is an online compiler and debugger tool for C, C++, Python, Java, PHP, Ruby, Perl,
C#, OCaml, VB, Swift, Pascal, Fortran, Haskell, Objective-C, Assembly, HTML, CSS, JS, SQLite, Prolog.
Code, Compile, Run and Debug online from anywhere in world.

*******************************************************************************/
#include <iostream>
#include <string>

using namespace std;

bool contains(const string &str, const string &searchTerm)
{
    // If the search term is a single character, treat it as a char search
    if (searchTerm.size() == 1)
    {
        return str.find(searchTerm[0]) != string::npos;
    }
    else
    { // Otherwise, treat it as a word search
        return str.find(searchTerm) != string::npos;
    }
}

int main()
{
    string input, searchTerm;

    cout << "Enter a string: ";
    getline(cin, input);

    cout << "Enter a character or word to search for: ";
    getline(cin, searchTerm);

    if (contains(input, searchTerm))
    {
        cout << "The search term '" << searchTerm << "' is present in the string." << endl;
    }
    else
    {
        cout << "The search term '" << searchTerm << "' is not present in the string." << endl;
    }

    return 0;
}