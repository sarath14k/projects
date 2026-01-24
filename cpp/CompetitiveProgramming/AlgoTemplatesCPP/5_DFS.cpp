#include <iostream>
#include <vector>

void dfsRecursive(int node, const std::vector<std::vector<int>>& graph, std::vector<bool>& visited) {
    // Mark the current node as visited
    visited[node] = true;
    std::cout << node << " "; // Process the node (e.g., print it)

    // Recur for all the vertices adjacent to this vertex
    for (int neighbor : graph[node]) {
        if (!visited[neighbor]) {
            dfsRecursive(neighbor, graph, visited);
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

    std::vector<bool> visited(numNodes, false); // Visited array

    std::cout << "DFS Recursive Traversal: ";
    dfsRecursive(0, graph, visited); // Start DFS from node 0
    std::cout << std::endl;

    return 0;
}
