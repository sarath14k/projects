#include <iostream>
#include <stack>
#include <unordered_map>
#include <string>

using namespace std;

// Merged Solution class for validating parentheses
class Solution {
public:
    bool isValid(string s) {
        stack<char> openParentheses;  // Stack to keep track of open parentheses
        unordered_map<char, char> matchingParentheses = {
            {')', '('},
            {']', '['},
            {'}', '{'},
        };
        
        // Iterate through each character in the input string
        for (const auto& currentChar : s) {
            // Check if the current character is a closing parenthesis
            if (matchingParentheses.find(currentChar) != matchingParentheses.end()) {
                // If the stack is empty, there's no corresponding opening parenthesis
                if (openParentheses.empty()) {
                    return false;
                }

                // Check if the top of the stack matches the expected opening parenthesis
                if (openParentheses.top() != matchingParentheses[currentChar]) {
                    return false;
                }

                // Pop the matched opening parenthesis from the stack
                openParentheses.pop();
            } else {
                // If it's an opening parenthesis, push it onto the stack
                openParentheses.push(currentChar);
            }
        }
        
        // Return true if no unmatched opening parentheses remain
        return openParentheses.empty();
    }
    /*
    Time Complexity: O(n), where n is the length of the input string s.
    Space Complexity: O(n), for the stack in the worst case when all characters are opening parentheses.
    */
};

// Main function to test the solution
int main() {
    Solution solution;

    // Test case
    string s = "([{}])";

    // Test the isValid method
    bool result = solution.isValid(s);
    cout << "Is the string valid? " << (result ? "Yes" : "No") << endl;

    return 0;
}
