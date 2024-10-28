#include <iostream>
#include <vector>
#include <stdexcept>

class MaxHeap {
private:
    std::vector<int> heap; // Store the heap elements

    // Helper function to maintain the max-heap property after insertion
    void heapifyUp(int index) {
        while (index > 0) {
            int parentIndex = (index - 1) / 2;
            if (heap[index] <= heap[parentIndex]) {
                break; // If the current node is in correct position
            }
            std::swap(heap[index], heap[parentIndex]); // Swap with parent
            index = parentIndex; // Move up the heap
        }
    }

    // Helper function to maintain the max-heap property after deletion
    void heapifyDown(int index) {
        int leftChild, rightChild, largest;

        while (true) {
            leftChild = 2 * index + 1; // Left child index
            rightChild = 2 * index + 2; // Right child index
            largest = index;

            // Check if left child exists and is greater than the current largest
            if (leftChild < heap.size() && heap[leftChild] > heap[largest]) {
                largest = leftChild;
            }
            // Check if right child exists and is greater than the current largest
            if (rightChild < heap.size() && heap[rightChild] > heap[largest]) {
                largest = rightChild;
            }
            // If the largest is still the current index, we're done
            if (largest == index) {
                break;
            }
            std::swap(heap[index], heap[largest]); // Swap with the largest
            index = largest; // Move down the heap
        }
    }

public:
    // Insert a new element into the heap
    void insert(int value) {
        heap.push_back(value); // Add the new value to the end
        heapifyUp(heap.size() - 1); // Restore heap property
    }

    // Delete the maximum element from the heap
    int deleteMax() {
        if (heap.empty()) {
            throw std::out_of_range("Heap is empty");
        }

        int maxValue = heap[0]; // Store the maximum value
        heap[0] = heap.back(); // Replace it with the last element
        heap.pop_back(); // Remove the last element
        if (!heap.empty()) {
            heapifyDown(0); // Restore heap property
        }
        return maxValue; // Return the maximum value
    }

    // Get the maximum element without removing it
    int getMax() const {
        if (heap.empty()) {
            throw std::out_of_range("Heap is empty");
        }
        return heap[0]; // Return the maximum value
    }

    // Check if the heap is empty
    bool isEmpty() const {
        return heap.empty();
    }

    // Get the size of the heap
    size_t size() const {
        return heap.size();
    }
};
int main() {
    MaxHeap maxHeap;

    // Insert elements
    maxHeap.insert(10);
    maxHeap.insert(20);
    maxHeap.insert(15);
    maxHeap.insert(30);
    maxHeap.insert(25);

    std::cout << "Max element: " << maxHeap.getMax() << std::endl; // Should print 30

    // Delete max elements
    while (!maxHeap.isEmpty()) {
        std::cout << "Deleted max: " << maxHeap.deleteMax() << std::endl;
    }

    return 0;
}
