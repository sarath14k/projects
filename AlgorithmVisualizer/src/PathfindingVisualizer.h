#ifndef PATHFINDINGVISUALIZER_H
#define PATHFINDINGVISUALIZER_H

#include <SFML/Graphics.hpp>
#include <vector>

class PathfindingVisualizer {
public:
    PathfindingVisualizer(int windowWidth, int windowHeight);

    void visualizeDijkstra();
    void dijkstra(const std::vector<std::vector<int>>& graph, int src);

private:
    sf::RenderWindow window;
    int windowWidth;
    int windowHeight;

    void drawGraph(const std::vector<std::vector<int>>& graph, const std::vector<int>& dist, int current);
};

#endif
