#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>

using namespace std;

// Function to perform Bubble Sort
void bubbleSort(vector<int>& arr) {
    int arraySize = arr.size(); // Get the size of the array
    for (int i = 0; i < arraySize - 1; i++) {
        for (int j = 0; j < arraySize - i - 1; j++) {
            // Swap if the element found is greater than the next element
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
            }
        }
        // Passes for Bubble Sort
        cout << "After pass " << i + 1 << ": ";
        for (int value : arr) cout << value << " ";
        cout << endl;
    }
    // Time Complexity:
    // Best Case: O(n)  (when the array is already sorted)
    // Average Case: O(n^2)
    // Worst Case: O(n^2) (when the array is sorted in reverse order)
    // Space Complexity: O(1)
}

// Function to perform Selection Sort
void selectionSort(vector<int>& arr) {
    int arraySize = arr.size(); // Get the size of the array
    for (int i = 0; i < arraySize - 1; i++) {
        int minIndex = i; // Find the index of the minimum element
        for (int j = i + 1; j < arraySize; j++) {
            if (arr[j] < arr[minIndex]) {
                minIndex = j; // Update minIndex if a smaller element is found
            }
        }
        swap(arr[i], arr[minIndex]); // Swap the found minimum element with the first element
        
        // Passes for Selection Sort
        cout << "After selecting element " << i + 1 << ": ";
        for (int value : arr) cout << value << " ";
        cout << endl;
    }
    // Time Complexity:
    // Best Case: O(n^2) (same for all cases as we always go through the array)
    // Average Case: O(n^2)
    // Worst Case: O(n^2)
    // Space Complexity: O(1)
}

// Function to perform Insertion Sort
void insertionSort(vector<int>& arr) {
    int arraySize = arr.size(); // Get the size of the array
    for (int i = 1; i < arraySize; i++) {
        int key = arr[i]; // Element to be inserted
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j]; // Move elements that are greater than key
            j--;
        }
        arr[j + 1] = key; // Insert the key at the correct position
        
        // Passes for Insertion Sort
        cout << "After inserting element " << key << ": ";
        for (int value : arr) cout << value << " ";
        cout << endl;
    }
    // Time Complexity:
    // Best Case: O(n)  (when the array is already sorted)
    // Average Case: O(n^2)
    // Worst Case: O(n^2) (when the array is sorted in reverse order)
    // Space Complexity: O(1)
}

// Function to merge two halves for Merge Sort
void merge(vector<int>& arr, int left, int mid, int right) {
    int leftSize = mid - left + 1; // Size of left half
    int rightSize = right - mid;    // Size of right half
    vector<int> leftArray(leftSize), rightArray(rightSize); // Temporary arrays

    // Copy data to temporary arrays leftArray[] and rightArray[]
    for (int i = 0; i < leftSize; i++)
        leftArray[i] = arr[left + i];
    for (int j = 0; j < rightSize; j++)
        rightArray[j] = arr[mid + 1 + j];

    int i = 0, j = 0, k = left; // Initial indexes for left, right and merged array
    while (i < leftSize && j < rightSize) {
        if (leftArray[i] <= rightArray[j]) {
            arr[k] = leftArray[i];
            i++;
        } else {
            arr[k] = rightArray[j];
            j++;
        }
        k++;
    }

    // Copy the remaining elements of leftArray[], if there are any
    while (i < leftSize) {
        arr[k] = leftArray[i];
        i++;
        k++;
    }

    // Copy the remaining elements of rightArray[], if there are any
    while (j < rightSize) {
        arr[k] = rightArray[j];
        j++;
        k++;
    }
}

// Function to perform Merge Sort
void mergeSort(vector<int>& arr, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2; // Find the midpoint

        mergeSort(arr, left, mid); // Sort first half
        mergeSort(arr, mid + 1, right); // Sort second half
        merge(arr, left, mid, right); // Merge the sorted halves
    }
}

// Function to perform Quick Sort
int partition(vector<int>& arr, int low, int high) {
    int pivot = arr[high]; // Pivot element
    int i = (low - 1); // Index of smaller element
    for (int j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++; // Increase index of smaller element
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]); // Swap the pivot element
    return (i + 1); // Return the partitioning index
}

void quickSort(vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high); // Partition the array

        quickSort(arr, low, pi - 1); // Recursively sort elements before partition
        quickSort(arr, pi + 1, high); // Recursively sort elements after partition
    }
}

// Function to print an array
void printArray(const vector<int>& arr) {
    for (int value : arr) {
        cout << value << " ";
    }
    cout << endl;
}

// Main function
int main() {
    vector<int> arr1 = {64, 34, 25, 12, 22, 11, 90};
    vector<int> arr2 = arr1; // Copy original array for Selection Sort
    vector<int> arr3 = arr1; // Copy original array for Insertion Sort
    vector<int> arr4 = arr1; // Copy original array for Merge Sort
    vector<int> arr5 = arr1; // Copy original array for Quick Sort

    cout << "Bubble Sort:" << endl;
    bubbleSort(arr1);

    cout << "\nSelection Sort:" << endl;
    selectionSort(arr2);

    cout << "\nInsertion Sort:" << endl;
    insertionSort(arr3);

    cout << "\nMerge Sort:" << endl;
    mergeSort(arr4, 0, arr4.size() - 1);
    printArray(arr4);

    cout << "\nQuick Sort:" << endl;
    quickSort(arr5, 0, arr5.size() - 1);
    printArray(arr5);

    return 0;
}
/*
    Time Complexity Table

    Bubble Sort:
    ------------------------
    | Case            | Time Complexity  | Space Complexity |
    |------------------|-----------------|------------------|
    | Best Case        | O(n)            | O(1)             |
    | Average Case     | O(n^2)          | O(1)             |
    | Worst Case       | O(n^2)          | O(1)             |
    ------------------------

    Selection Sort:
    ------------------------
    | Case            | Time Complexity  | Space Complexity |
    |------------------|-----------------|------------------|
    | Best Case        | O(n^2)          | O(1)             |
    | Average Case     | O(n^2)          | O(1)             |
    | Worst Case       | O(n^2)          | O(1)             |
    ------------------------

    Insertion Sort:
    ------------------------
    | Case            | Time Complexity  | Space Complexity |
    |------------------|-----------------|------------------|
    | Best Case        | O(n)            | O(1)             |
    | Average Case     | O(n^2)          | O(1)             |
    | Worst Case       | O(n^2)          | O(1)             |
    ------------------------

    Merge Sort:
    ------------------------
    | Case            | Time Complexity  | Space Complexity |
    |------------------|-----------------|------------------|
    | Best Case        | O(n log n)      | O(n)             |
    | Average Case     | O(n log n)      | O(n)             |
    | Worst Case       | O(n log n)      | O(n)             |
    ------------------------

    Quick Sort:
    ------------------------
    | Case            | Time Complexity  | Space Complexity |
    |------------------|-----------------|------------------|
    | Best Case        | O(n log n)      | O(log n)         |
    | Average Case     | O(n log n)      | O(log n)         |
    | Worst Case       | O(n^2)          | O(log n)         |
    ------------------------
*/
