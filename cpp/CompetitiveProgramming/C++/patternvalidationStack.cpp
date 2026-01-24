#include <iostream>
#include "bits/stdc++.h"
using namespace std;

bool patternValid(const string &pattern)
{
    stack<char> st;
    int length = pattern.length();
    for (char s : pattern)
    {

        if (s == '}')
        {
            if (st.top() == '{')
            {
                st.pop();
            }
            else
            {
                return false;
            }
        }
        else if (s == ']')
        {
            if (st.top() == '[')
            {
                st.pop();
            }
            else
            {
                return false;
            }
        }
        else if (s == ')')
        {
            if (st.top() == '(')
            {
                st.pop();
            }
            else
            {
                return false;
            }
        }
        else
        {
            st.push(s);
        }
    }

    return st.empty(); // stack will be empty if all braces matches
}
int main()
{

    string pattern = "{}[]()";
    // string pattern = "{[()]}";
    bool status = patternValid(pattern);
    status ? cout << "valid" << endl : cout << "invalid" << endl;
    return 0;
}

/*

bool patternValid(const string &pattern) {
    stack<char> st;
    for (char s : pattern) {
        if (s == '}' || s == ']' || s == ')') {
            if (st.empty()) {
                return false; // Stack should not be empty if a closing brace is found
            }
            char top = st.top();
            if ((s == '}' && top == '{') || (s == ']' && top == '[') || (s == ')' && top == '(')) {
                st.pop();
            } else {
                return false;
            }
        } else {
            st.push(s);
        }
    }
    return st.empty(); // Stack should be empty if all braces are matched
}

int main() {
    string pattern = "{[()]}";
    bool status = patternValid(pattern);
    cout << (status ? "valid" : "invalid") << endl;
    return 0;
}


*/