#include <iostream>
#include <sstream>   // For stringstream
#include <algorithm> // For std::reverse
#include <string>

std::string reverseWordsInSentence(const std::string &sentence)
{
    std::stringstream ss(sentence); // Input string stream for splitting words
    std::string word;
    std::string result = "";

    // Read each word from the sentence
    while (ss >> word)
    {
        // Reverse the current word
        std::reverse(word.begin(), word.end());

        // Append the reversed word to the result with a space
        result += word + " ";
    }

    // Remove the trailing space at the end (if any)
    if (!result.empty())
    {
        result.pop_back();
    }

    return result;
}

int main()
{
    std::string sentence = "Hello World from C++";
    std::string reversedSentence = reverseWordsInSentence(sentence);

    std::cout << "Original Sentence: " << sentence << std::endl;
    std::cout << "Reversed Words Sentence: " << reversedSentence << std::endl;

    return 0;
}
