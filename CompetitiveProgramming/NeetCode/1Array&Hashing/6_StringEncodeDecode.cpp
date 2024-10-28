#include <iostream>
#include <vector>
#include <string>
using namespace std;

// Original Solution class for encoding and decoding strings
class OriginalSolution {
public:
    // Function to encode a vector of strings into a single string
    string encode(vector<string>& stringList) {
        string encodedString = "";
        
        // Loop through each string in the vector
        for (int i = 0; i < stringList.size(); i++) {
            string currentString = stringList[i];
            encodedString += to_string(currentString.size()) + "#" + currentString;  // Concatenate length and string with a separator
        }
        
        return encodedString;  // Return the encoded string
    }

    // Function to decode a single string back into a vector of strings
    vector<string> decode(string encodedString) {
        vector<string> decodedStrings;
        
        int currentIndex = 0;
        while (currentIndex < encodedString.size()) {
            int separatorIndex = currentIndex;
            // Find the separator position
            while (encodedString[separatorIndex] != '#') {
                separatorIndex++;
            }
            int stringLength = stoi(encodedString.substr(currentIndex, separatorIndex - currentIndex));  // Get the length of the next string
            string decodedString = encodedString.substr(separatorIndex + 1, stringLength);    // Extract the string using the length
            decodedStrings.push_back(decodedString);  // Add the decoded string to the result
            currentIndex = separatorIndex + 1 + stringLength;  // Move to the next encoded string
        }
        
        return decodedStrings;  // Return the decoded vector of strings
    }
    /*
    Time Complexity: O(n), where n is the total number of characters in the strings.
    Space Complexity: O(n), for the encoded string and the vector of decoded strings.
    */
};

// Optimized Solution class for encoding and decoding strings
class Solution {
public:
    // Function to encode a vector of strings into a single string
    string encode(vector<string>& stringList) {
        string encodedString;
        encodedString.reserve(1000); // Improvement: Reserve space to optimize memory allocation
        
        // Loop through each string in the vector
        for (const auto& currentString : stringList) {
            encodedString += to_string(currentString.size()) + '#' + currentString; // Concatenate length and string with a separator
        }
        
        return encodedString; // Return the encoded string
    }

    // Function to decode a single string back into a vector of strings
    vector<string> decode(string encodedString) {
        vector<string> decodedStrings;
        int currentIndex = 0;

        // While there are still characters to read in the string
        while (currentIndex < encodedString.size()) {
            int separatorIndex = encodedString.find('#', currentIndex); // Improvement: Use find to locate the separator
            int stringLength = stoi(encodedString.substr(currentIndex, separatorIndex - currentIndex)); // Get the length of the next string
            decodedStrings.push_back(encodedString.substr(separatorIndex + 1, stringLength)); // Extract the string using the length
            currentIndex = separatorIndex + 1 + stringLength; // Move to the next encoded string
        }
        
        return decodedStrings; // Return the decoded vector of strings
    }
    /*
    Time Complexity: O(n), where n is the total number of characters in the strings.
    Space Complexity: O(n), for the encoded string and the vector of decoded strings.
    */
};

// Simple main function to test both versions
int main() {
    OriginalSolution originalSol;
    Solution optimizedSol;

    // Test case: Simple example
    vector<string> stringList = {"hello", "world", "this", "is", "an", "encoder"};

    // Test the original solution
    cout << "Original Solution: Encoded string: " << originalSol.encode(stringList) << endl;
    vector<string> decodedOriginal = originalSol.decode(originalSol.encode(stringList));
    cout << "Decoded strings: ";
    for (const auto& decodedString : decodedOriginal) {
        cout << decodedString << " ";
    }
    cout << endl;

    // Test the optimized solution
    cout << "Optimized Solution: Encoded string: " << optimizedSol.encode(stringList) << endl;
    vector<string> decodedOptimized = optimizedSol.decode(optimizedSol.encode(stringList));
    cout << "Decoded strings: ";
    for (const auto& decodedString : decodedOptimized) {
        cout << decodedString << " ";
    }
    cout << endl;

    return 0;
}
