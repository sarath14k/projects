#include <iostream>
#include <queue>
using namespace std;

class MedianFinder {
public:
    // Constructor to initialize the median finder
    MedianFinder() { }

    // Function to add a number into the data structure
    void addNum(int num) {
        // If the lower half is larger, rebalance
        if (lowerHalf.size() > higherHalf.size()) {
            if (lowerHalf.top() > num) {
                // Move the top of the lower half to the higher half
                higherHalf.push(lowerHalf.top());
                lowerHalf.pop();
                lowerHalf.push(num);
            } else {
                higherHalf.push(num);
            }
        } else {
            // If the higher half is larger or equal, rebalance
            if (higherHalf.empty() || num <= higherHalf.top()) {
                lowerHalf.push(num);
            } else {
                lowerHalf.push(higherHalf.top());
                higherHalf.pop();
                higherHalf.push(num);
            }
        }
    }

    // Function to find the median of current numbers
    double findMedian() {
        if (lowerHalf.size() == higherHalf.size()) {
            // If even, return the average of the two middle numbers
            return lowerHalf.top() + (higherHalf.top() - lowerHalf.top()) / 2.0;
        } else {
            // If odd, return the top of the larger half
            return lowerHalf.size() > higherHalf.size() ? lowerHalf.top() : higherHalf.top();
        }
    }

private:
    // Max heap for the lower half
    priority_queue<int> lowerHalf;
    // Min heap for the higher half
    priority_queue<int, vector<int>, greater<int>> higherHalf;
};

/*
Time Complexity:
- addNum: O(log n), where n is the number of elements in the data structure.
- findMedian: O(1).

Space Complexity: O(n), where n is the number of elements in the data structure.
*/

int main() {
    MedianFinder medianFinder;

    // Adding numbers to the median finder
    medianFinder.addNum(1);
    medianFinder.addNum(2);
    cout << "Median after adding 1 and 2: " << medianFinder.findMedian() << endl; // Output: 1.5

    medianFinder.addNum(3);
    cout << "Median after adding 3: " << medianFinder.findMedian() << endl; // Output: 2.0

    return 0;
}
