#include <iostream>
#include <vector>
#include <unordered_map>
#include <queue>
#include <algorithm>
using namespace std;

// Original Solution class to find the top K frequent elements
class OriginalSolution {
public:
    // Function to find the top K frequent elements
    vector<int> topKFrequent(vector<int>& nums, int k) {
        unordered_map<int, int> count;  // Map to store the frequency of each element
        for (int num : nums) {
            count[num]++;  // Increment the count for each element
        }

        // Create a vector of pairs to store frequencies and corresponding elements
        vector<pair<int, int>> arr;
        for (const auto& p : count) {
            arr.push_back({p.second, p.first});  // Store frequency and element as a pair
        }

        // Sort the vector in descending order of frequency
        sort(arr.rbegin(), arr.rend());

        // Collect the top K frequent elements
        vector<int> res;
        for (int i = 0; i < k; ++i) {
            res.push_back(arr[i].second);
        }
        return res;  // Return the result vector
    }
    /*
    Time Complexity: O(n log n) due to the sorting step, where n is the number of unique elements.
    Space Complexity: O(n) for the hash map and vector storing unique elements.
    */
};

// Optimized Solution class to find the top K frequent elements
class Solution {
public:
    // Optimized function to find the top K frequent elements
    vector<int> topKFrequent(vector<int>& nums, int k) {
        unordered_map<int, int> count;  // Map to store the frequency of each element
        for (int num : nums) {
            count[num]++;  // Same as original: Increment the count for each element
        }

        // Improvement: Use a priority queue (min-heap) for better performance
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> minHeap;

        // Insert frequencies and elements into the min-heap
        for (const auto& p : count) {
            minHeap.push({p.second, p.first});  // Store frequency and element as a pair
            if (minHeap.size() > k) {
                minHeap.pop();  // Keep only the top K frequent elements in the heap
            }
        }

        // Collect the top K frequent elements from the min-heap
        vector<int> res;
        while (!minHeap.empty()) {
            res.push_back(minHeap.top().second);  // Extract elements from the heap
            minHeap.pop();
        }

        reverse(res.begin(), res.end());  // Since we used a min-heap, reverse the result
        return res;  // Return the result vector
    }
    /*
    Time Complexity: O(n log k) where n is the number of elements in nums and k is the number of top frequent elements.
    Space Complexity: O(n) for the hash map storing the frequencies, and O(k) for the min-heap.
    */
};

// Simple main function to test both versions
int main() {
    // Create instances of both Original and Optimized Solution classes
    OriginalSolution originalSol;
    Solution optimizedSol;  // Using just "Solution" for the optimized version

    // Test case: Simple example
    vector<int> nums = {1, 1, 1, 2, 2, 3};
    int k = 2;

    // Test the original solution
    cout << "Original Solution: Top " << k << " frequent elements:" << endl;
    vector<int> result1 = originalSol.topKFrequent(nums, k);
    for (int num : result1) {
        cout << num << " ";
    }
    cout << endl;

    // Test the optimized solution
    cout << "Optimized Solution: Top " << k << " frequent elements:" << endl;
    vector<int> result2 = optimizedSol.topKFrequent(nums, k);
    for (int num : result2) {
        cout << num << " ";
    }
    cout << endl;

    return 0;
}
