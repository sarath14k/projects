#include <iostream>
#include <string>
#include <unordered_map>

char mostOccurringChar(const std::string& str) {
    std::unordered_map<char, int> charCount;
    char mostOccurring = '\0';
    int maxCount = 0;

    for (char c : str) {
        charCount[c]++;
        if (charCount[c] > maxCount) {
            maxCount = charCount[c];
            mostOccurring = c;
        }
    }

    return mostOccurring;
}

int main() {
    std::string str = "hello world";
    char mostOccurring = mostOccurringChar(str);
    std::cout << "The most occurring character in \"" << str << "\" is: " << mostOccurring << std::endl;

    return 0;
}
