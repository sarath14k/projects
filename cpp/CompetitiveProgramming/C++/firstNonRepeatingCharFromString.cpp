#include <iostream>
#include <unordered_map>
#include <string>

char firstNonRepeatingCharacter(const std::string &str)
{
    std::unordered_map<char, int> charCount;

    // Count the frequency of each character
    for (char ch : str)
    {
        charCount[ch]++;
    }

    // Find the first non-repeating character
    for (char ch : str)
    {
        if (charCount[ch] == 1)
        {
            return ch; // Return the first non-repeating character
        }
    }

    return '\0'; // Return null character if there is no non-repeating character
}

int main()
{
    std::string input = "swiss";
    char result = firstNonRepeatingCharacter(input);

    if (result != '\0')
    {
        std::cout << "The first non-repeating character is: " << result << std::endl; // Output: w
    }
    else
    {
        std::cout << "There are no non-repeating characters." << std::endl;
    }

    return 0;
}
