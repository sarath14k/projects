#ifndef SORTING_VISUALIZER_H
#define SORTING_VISUALIZER_H

#include <SFML/Graphics.hpp>
#include <vector>

class SortingVisualizer {
public:
    SortingVisualizer(int windowWidth, int windowHeight);
    
    void visualizeBubbleSort(std::vector<int>& arr);
    void visualizeQuickSort(std::vector<int>& arr);
    void visualizeMergeSort(std::vector<int>& arr);
    void visualizeHeapSort(std::vector<int>& arr);

private:
    sf::RenderWindow window;
    sf::Font font;
    int windowWidth;
    int windowHeight;

    void drawArray(const std::vector<int>& arr);
    void quickSort(std::vector<int>& arr, int low, int high);
    int partition(std::vector<int>& arr, int low, int high);
    void mergeSort(std::vector<int>& arr, int left, int right);
    void merge(std::vector<int>& arr, int left, int mid, int right);
    void heapify(std::vector<int>& arr, int n, int i);
};

#endif

