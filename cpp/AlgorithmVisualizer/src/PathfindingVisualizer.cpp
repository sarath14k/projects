#include "PathfindingVisualizer.h"
#include <queue>
#include <limits>
#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>
#include <vector>
#include <cmath>

PathfindingVisualizer::PathfindingVisualizer(int windowWidth, int windowHeight) 
    : window(sf::VideoMode(windowWidth, windowHeight), "Dijkstra Visualizer"),
      windowWidth(windowWidth), windowHeight(windowHeight) {}

void PathfindingVisualizer::visualizeDijkstra() {
    // Graph as an adjacency matrix (6 nodes, weighted edges)
    std::vector<std::vector<int>> graph = {
        {0, 10, 20, 0, 0, 0},
        {10, 0, 0, 50, 10, 0},
        {20, 0, 0, 20, 33, 0},
        {0, 50, 20, 0, 20, 2},
        {0, 10, 33, 20, 0, 1},
        {0, 0, 0, 2, 1, 0}
    };
    
    // Call Dijkstra's algorithm to visualize starting from node 0
    dijkstra(graph, 0);
}

void PathfindingVisualizer::dijkstra(const std::vector<std::vector<int>>& graph, int src) {
    int V = graph.size();
    std::vector<int> dist(V, std::numeric_limits<int>::max());
    dist[src] = 0;

    std::priority_queue<std::pair<int, int>, std::vector<std::pair<int, int>>, std::greater<>> pq;
    pq.push({0, src});

    while (!pq.empty()) {
        int u = pq.top().second;
        pq.pop();

        // Redraw graph
        window.clear();
        drawGraph(graph, dist, u); // Update graph with current distances and node
        window.display();
        sf::sleep(sf::milliseconds(100)); // Pause for animation effect

        // Relaxation of adjacent nodes
        for (int v = 0; v < V; ++v) {
            if (graph[u][v] && dist[u] + graph[u][v] < dist[v]) {
                dist[v] = dist[u] + graph[u][v];
                pq.push({dist[v], v});
            }
        }
    }
}

// Function to draw the graph and the nodes during the visualization
void PathfindingVisualizer::drawGraph(const std::vector<std::vector<int>>& graph, const std::vector<int>& dist, int current) {
    int V = graph.size();
    
    // Predefined positions for the nodes on the window
    std::vector<sf::Vector2f> nodePositions = {
        {100, 100}, {300, 100}, {500, 100},
        {100, 300}, {300, 300}, {500, 300}
    };

    // Draw edges first
    for (int u = 0; u < V; ++u) {
        for (int v = u + 1; v < V; ++v) {
            if (graph[u][v] > 0) {
                sf::Vertex line[] = {
                    sf::Vertex(nodePositions[u], sf::Color::White),
                    sf::Vertex(nodePositions[v], sf::Color::White)
                };
                window.draw(line, 2, sf::Lines);
            }
        }
    }

    // Draw nodes and update distances
    for (int i = 0; i < V; ++i) {
        sf::CircleShape node(20);
        node.setPosition(nodePositions[i].x - 20, nodePositions[i].y - 20); // Center the circle
        node.setFillColor(i == current ? sf::Color::Green : sf::Color::Blue); // Highlight current node

        window.draw(node);

        // Display distance values above the nodes
        sf::Font font;
        if (!font.loadFromFile("arial.ttf")) {
            // Handle font loading error
        }

        sf::Text distText;
        distText.setFont(font);
        distText.setCharacterSize(20);
        distText.setFillColor(sf::Color::White);

        if (dist[i] == std::numeric_limits<int>::max()) {
            distText.setString("Inf");
        } else {
            distText.setString(std::to_string(dist[i]));
        }

        distText.setPosition(nodePositions[i].x - 10, nodePositions[i].y - 40); // Position above the node
        window.draw(distText);
    }
}
