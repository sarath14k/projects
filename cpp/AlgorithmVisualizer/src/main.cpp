#include <SFML/Graphics.hpp>
#include "SortingVisualizer.h"
#include "PathfindingVisualizer.h"
#include <iostream>
#include <vector>
#include <cstdlib>

int main() {
    int windowWidth = 800;
    int windowHeight = 600;

    // Sorting Visualizer
    SortingVisualizer sortingVisualizer(windowWidth, windowHeight);

    // Pathfinding Visualizer
    PathfindingVisualizer pathfindingVisualizer(windowWidth, windowHeight);

    // Random array for sorting visualization
    std::vector<int> arr(100);
    for (int i = 0; i < 100; i++) {
        arr[i] = rand() % 100 + 1;
    }

    int choice;
    
    std::cout << "Choose an algorithm to visualize:\n";
    std::cout << "1. Bubble Sort\n";
    std::cout << "2. Quick Sort\n";
    std::cout << "3. Merge Sort\n";
    std::cout << "4. Heap Sort\n";
    std::cout << "5. Dijkstra's Algorithm\n";
    std::cout << "Enter your choice (1-5): ";
    std::cin >> choice;

    switch (choice) {
        case 1:
            std::cout << "Visualizing Bubble Sort...\n";
            sortingVisualizer.visualizeBubbleSort(arr);
            break;
        case 2:
            std::cout << "Visualizing Quick Sort...\n";
            sortingVisualizer.visualizeQuickSort(arr);
            break;
        case 3:
            std::cout << "Visualizing Merge Sort...\n";
            sortingVisualizer.visualizeMergeSort(arr);
            break;
        case 4:
            std::cout << "Visualizing Heap Sort...\n";
            sortingVisualizer.visualizeHeapSort(arr);
            break;
        case 5:
            std::cout << "Visualizing Dijkstra's Algorithm...\n";
            pathfindingVisualizer.visualizeDijkstra();
            break;
        default:
            std::cout << "Invalid choice. Please enter a number between 1 and 5.\n";
            break;
    }

    return 0;
}

