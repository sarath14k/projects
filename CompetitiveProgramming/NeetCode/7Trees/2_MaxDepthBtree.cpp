#include <iostream>
#include <queue>

using namespace std;

/**
 * Definition for a binary tree node.
 */
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

class Solution {
public:
    // Function to invert a binary tree
    TreeNode* invertTree(TreeNode* root) {
        if (root == nullptr) return nullptr; // Base case: if the node is null, return null

        // Create a new node with the current root's value
        TreeNode* node = new TreeNode(root->val);
        
        // Recursively invert the left and right subtrees
        node->right = invertTree(root->left);
        node->left = invertTree(root->right);

        return node; // Return the new inverted tree
    }

    // Function to print the tree in level order
    void printTree(TreeNode* root) {
        if (!root) return; // If the node is null, return
        queue<TreeNode*> q; // Queue to hold nodes for level order traversal
        q.push(root); // Start with the root node
        
        while (!q.empty()) {
            TreeNode* current = q.front(); // Get the front node
            q.pop(); // Remove the front node
            cout << current->val << " "; // Print the value
            
            // Add child nodes to the queue
            if (current->left) q.push(current->left);
            if (current->right) q.push(current->right);
        }
        cout << endl; // Print a new line after the tree values
    }
};

int main() {
    // Create a simple tree: 
    //        4
    //       / \
    //      2   7
    //     / \ / \
    //    1  3 6  9
    TreeNode* root = new TreeNode(4);
    root->left = new TreeNode(2);
    root->right = new TreeNode(7);
    root->left->left = new TreeNode(1);
    root->left->right = new TreeNode(3);
    root->right->left = new TreeNode(6);
    root->right->right = new TreeNode(9);

    Solution solution;
    cout << "Original tree (level order): ";
    solution.printTree(root); // Print original tree

    TreeNode* invertedRoot = solution.invertTree(root); // Invert the tree
    cout << "Inverted tree (level order): ";
    solution.printTree(invertedRoot); // Print inverted tree

    return 0; // Return 0 to indicate successful execution
}

/*
Time Complexity: O(n), where n is the number of nodes in the tree.
Space Complexity: O(h), where h is the height of the tree due to the recursive call stack.
*/
