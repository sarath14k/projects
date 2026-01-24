#include <iostream>
#include <vector>
#include <unordered_set>

std::pair<int, int> largestConsecutiveSubarray(const std::vector<int> &arr)
{
    std::unordered_set<int> elements(arr.begin(), arr.end()); // Create a set from the array
    int maxLength = 0;                                        // Maximum length of consecutive integers
    int start = 0;                                            // Starting element of the longest consecutive sub-array

    for (int num : arr)
    {
        // Check if it is the start of a sequence
        if (elements.find(num) != elements.end())
        {
            int currentNum = num;
            int currentLength = 0;

            // Check for consecutive numbers
            while (elements.find(currentNum) != elements.end())
            {
                currentLength++;
                elements.erase(currentNum); // Remove it from the set to avoid counting again
                currentNum++;
            }

            // Update max length and start point if needed
            if (currentLength > maxLength)
            {
                maxLength = currentLength;
                start = num; // Update starting point of the longest consecutive sub-array
            }
        }
    }

    return {start, maxLength}; // Return the starting point and length of the longest consecutive sub-array
}

int main()
{
    std::vector<int> arr = {1, 9, 3, 4, 2, 20, 5, 6}; // Example array
    auto result = largestConsecutiveSubarray(arr);

    if (result.second > 0)
    {
        std::cout << "Largest consecutive subarray starts at: " << result.first
                  << " with length: " << result.second << std::endl;
    }
    else
    {
        std::cout << "No consecutive subarray found." << std::endl;
    }

    return 0;
}
