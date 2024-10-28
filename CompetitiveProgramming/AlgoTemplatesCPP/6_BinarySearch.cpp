#include <iostream>
#include <vector>

int binarySearch(const std::vector<int>& arr, int target) {
    int left = 0;
    int right = arr.size() - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2; // Prevent overflow

        if (arr[mid] == target) {
            return mid; // Target found, return index
        } 
        else if (arr[mid] < target) {
            left = mid + 1; // Search in the right half
        } 
        else {
            right = mid - 1; // Search in the left half
        }
    }

    return -1; // Target not found
}

int main() {
    // Example usage
    std::vector<int> arr = {1, 2, 3, 4, 5, 6, 7, 8, 9}; // Sorted array
    int target = 5;

    int result = binarySearch(arr, target);
    
    if (result != -1) {
        std::cout << "Target found at index: " << result << std::endl;
    } else {
        std::cout << "Target not found" << std::endl;
    }

    return 0;
}

#include <iostream>
#include <vector>

int binarySearchFirstOccurrence(const std::vector<int>& arr, int target) {
    int left = 0;
    int right = arr.size() - 1;
    int firstOccurrence = -1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target) {
            firstOccurrence = mid; // Update the first occurrence
            right = mid - 1; // Continue searching in the left half
        } 
        else if (arr[mid] < target) {
            left = mid + 1;
        } 
        else {
            right = mid - 1;
        }
    }

    return firstOccurrence; // Return the index of the first occurrence
}

int main() {
    // Example usage
    std::vector<int> arr = {1, 2, 2, 2, 3, 4, 5}; // Sorted array with duplicates
    int target = 2;

    int result = binarySearchFirstOccurrence(arr, target);
    
    if (result != -1) {
        std::cout << "First occurrence of target found at index: " << result << std::endl;
    } else {
        std::cout << "Target not found" << std::endl;
    }

    return 0;
}


#include <iostream>
#include <vector>

int binarySearchLastOccurrence(const std::vector<int>& arr, int target) {
    int left = 0;
    int right = arr.size() - 1;
    int lastOccurrence = -1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target) {
            lastOccurrence = mid; // Update the last occurrence
            left = mid + 1; // Continue searching in the right half
        } 
        else if (arr[mid] < target) {
            left = mid + 1;
        } 
        else {
            right = mid - 1;
        }
    }

    return lastOccurrence; // Return the index of the last occurrence
}

int main() {
    // Example usage
    std::vector<int> arr = {1, 2, 2, 2, 3, 4, 5}; // Sorted array with duplicates
    int target = 2;

    int result = binarySearchLastOccurrence(arr, target);
    
    if (result != -1) {
        std::cout << "Last occurrence of target found at index: " << result << std::endl;
    } else {
        std::cout << "Target not found" << std::endl;
    }

    return 0;
}
