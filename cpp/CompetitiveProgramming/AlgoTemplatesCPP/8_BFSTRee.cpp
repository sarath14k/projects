#include <iostream>
#include <vector>
#include <queue>

struct TreeNode {
    int val;
    std::vector<TreeNode*> children; // Adjust based on tree structure

    TreeNode(int x) : val(x) {}
};

void bfsTree(TreeNode* root) {
    if (!root) return; // Handle empty tree

    std::queue<TreeNode*> q; // Queue for BFS
    q.push(root);

    while (!q.empty()) {
        TreeNode* node = q.front();
        q.pop();
        std::cout << node->val << " "; // Process the node (e.g., print it)

        // Enqueue all children
        for (TreeNode* child : node->children) {
            q.push(child);
        }
    }
}

int main() {
    // Example usage
    TreeNode* root = new TreeNode(1);
    TreeNode* child1 = new TreeNode(2);
    TreeNode* child2 = new TreeNode(3);
    root->children.push_back(child1);
    root->children.push_back(child2);

    std::cout << "BFS Tree Traversal: ";
    bfsTree(root); // Start BFS from the root
    std::cout << std::endl;

    // Clean up dynamically allocated memory (if necessary)
    delete child1;
    delete child2;
    delete root;

    return 0;
}
