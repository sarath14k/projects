#include "SortingVisualizer.h"
#include <iostream>
#include <SFML/System.hpp>
#include <SFML/Graphics.hpp>

SortingVisualizer::SortingVisualizer(int windowWidth, int windowHeight) 
    : window(sf::VideoMode(windowWidth, windowHeight), "Sorting Visualizer"),
      windowWidth(windowWidth), windowHeight(windowHeight) { // Initialize member variables
    // Load font
   if (!font.loadFromFile("fonts/arial.ttf")) {
    std::cerr << "Error loading font from 'fonts/arial.ttf'" << std::endl;
}

}
void SortingVisualizer::visualizeBubbleSort(std::vector<int>& arr) {
    // Same as before
}

void SortingVisualizer::visualizeQuickSort(std::vector<int>& arr) {
    quickSort(arr, 0, arr.size() - 1);
}

void SortingVisualizer::visualizeMergeSort(std::vector<int>& arr) {
    mergeSort(arr, 0, arr.size() - 1);
}

void SortingVisualizer::visualizeHeapSort(std::vector<int>& arr) {
    int n = arr.size();
    
    // Build heap (rearrange array)
    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(arr, n, i);

    // Extract elements one by one from heap
    for (int i = n - 1; i > 0; i--) {
        std::swap(arr[0], arr[i]);
        
        // Redraw after each extraction
        window.clear();
        drawArray(arr);
        window.display();
        sf::sleep(sf::milliseconds(100));

        // Heapify the root
        heapify(arr, i, 0);
    }
}

void SortingVisualizer::quickSort(std::vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);

        // Redraw after partitioning
        window.clear();
        drawArray(arr);
        window.display();
        sf::sleep(sf::milliseconds(100));

        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

int SortingVisualizer::partition(std::vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = (low - 1);

    for (int j = low; j <= high - 1; j++) {
        if (arr[j] < pivot) {
            i++;
            std::swap(arr[i], arr[j]);
        }
    }
    std::swap(arr[i + 1], arr[high]);
    return (i + 1);
}

void SortingVisualizer::mergeSort(std::vector<int>& arr, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;

        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        merge(arr, left, mid, right);

        // Redraw after each merge
        window.clear();
        drawArray(arr);
        window.display();
        sf::sleep(sf::milliseconds(100));
    }
}

void SortingVisualizer::merge(std::vector<int>& arr, int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;

    std::vector<int> L(n1), R(n2);
    for (int i = 0; i < n1; i++) L[i] = arr[left + i];
    for (int i = 0; i < n2; i++) R[i] = arr[mid + 1 + i];

    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) arr[k++] = L[i++];
        else arr[k++] = R[j++];
    }

    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
}

void SortingVisualizer::heapify(std::vector<int>& arr, int n, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    if (left < n && arr[left] > arr[largest]) largest = left;
    if (right < n && arr[right] > arr[largest]) largest = right;

    if (largest != i) {
        std::swap(arr[i], arr[largest]);

        // Redraw after swap
        window.clear();
        drawArray(arr);
        window.display();
        sf::sleep(sf::milliseconds(100));

        heapify(arr, n, largest);
    }
}

void SortingVisualizer::drawArray(const std::vector<int>& arr) {
    float barWidth = static_cast<float>(windowWidth) / arr.size();

    for (std::vector<int>::size_type i = 0; i < arr.size(); i++) {
        sf::RectangleShape bar(sf::Vector2f(barWidth - 2, arr[i] * 5));
        bar.setPosition(i * barWidth, windowHeight - arr[i] * 5);
        bar.setFillColor(sf::Color::Green);
        window.draw(bar);
    }
}
