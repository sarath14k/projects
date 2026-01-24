#include <iostream>
#include <vector>
#include <queue>

void bfs(int startNode, const std::vector<std::vector<int>>& graph) {
    std::vector<bool> visited(graph.size(), false); // Visited array
    std::queue<int> q; // Queue for BFS

    q.push(startNode); // Start BFS from the starting node
    visited[startNode] = true;

    while (!q.empty()) {
        int node = q.front();
        q.pop();
        std::cout << node << " "; // Process the node (e.g., print it)

        // Explore all unvisited neighbors
        for (int neighbor : graph[node]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true; // Mark as visited
                q.push(neighbor); // Add to the queue
            }
        }
    }
}

int main() {
    // Example usage
    int numNodes = 5; // Number of nodes in the graph
    std::vector<std::vector<int>> graph(numNodes);

    // Example edges (undirected graph)
    graph[0] = {1, 2};
    graph[1] = {0, 3, 4};
    graph[2] = {0};
    graph[3] = {1};
    graph[4] = {1};

    std::cout << "BFS Traversal: ";
    bfs(0, graph); // Start BFS from node 0
    std::cout << std::endl;

    return 0;
}
