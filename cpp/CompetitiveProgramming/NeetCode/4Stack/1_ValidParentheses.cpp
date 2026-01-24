#include <iostream>
#include <stack>
#include <unordered_map>
#include <string>

using namespace std;

class Solution {
public:
    bool isValid(string s) {
        stack<char> stk;  // Stack to keep track of open parentheses
        unordered_map<char, char> pairs = {
            {')', '('},
            {']', '['},
            {'}', '{'}
        };

        for (const auto& ch : s) {
            if (pairs.find(ch) != pairs.end()) {  // If 'ch' is a closing bracket
                if (stk.empty() || stk.top() != pairs[ch]) {  // Stack empty or no match
                    return false;
                }
                stk.pop();  // Matching pair found, pop from stack
            } else {
                stk.push(ch);  // Push open brackets onto the stack
            }
        }

        return stk.empty();  // True if all brackets matched
    }

    /*
    Time Complexity: O(n), where n is the length of the input string s, since we process each character once.
    Space Complexity: O(n), in the worst case, all characters are open parentheses and need to be stored in the stack.
    */
};

int main() {
    Solution solution;
    string s = "([{}])";
    bool result = solution.isValid(s);
    cout << "Is the string valid? " << (result ? "Yes" : "No") << endl;

    return 0;
}
