#include <iostream>

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
    // Function to check if subRoot is a subtree of root
    bool isSubtree(TreeNode* root, TreeNode* subRoot) {
        if (!subRoot) {
            return true; // An empty tree is always a subtree
        }
        if (!root) {
            return false; // Non-empty subRoot cannot be a subtree of an empty root
        }

        // Check if the trees rooted at root and subRoot are the same
        if (sameTree(root, subRoot)) {
            return true; // If they are the same, subRoot is a subtree
        }
        // Recursively check left and right subtrees
        return isSubtree(root->left, subRoot) || isSubtree(root->right, subRoot);
    }

    // Helper function to check if two trees are the same
    bool sameTree(TreeNode* root, TreeNode* subRoot) {
        if (!root && !subRoot) {
            return true; // Both trees are empty
        }
        if (root && subRoot && root->val == subRoot->val) {
            // Recursively check left and right subtrees
            return sameTree(root->left, subRoot->left) && sameTree(root->right, subRoot->right);
        }
        return false; // Trees are not the same
    }
};

int main() {
    // Create main tree: 
    //        3
    //       / \
    //      4   5
    //     / \
    //    1   2
    TreeNode* root = new TreeNode(3);
    root->left = new TreeNode(4);
    root->right = new TreeNode(5);
    root->left->left = new TreeNode(1);
    root->left->right = new TreeNode(2);

    // Create subtree:
    //        4
    //       / \
    //      1   2
    TreeNode* subRoot = new TreeNode(4);
    subRoot->left = new TreeNode(1);
    subRoot->right = new TreeNode(2);

    Solution solution;
    bool result = solution.isSubtree(root, subRoot); // Check if subRoot is a subtree of root

    cout << "Is subRoot a subtree of root? " << (result ? "Yes" : "No") << endl; // Print result

    return 0; // Return 0 to indicate successful execution
}

/*
Time Complexity: O(m * n), where m and n are the number of nodes in root and subRoot, respectively. 
In the worst case, each node in root is compared with every node in subRoot.
Space Complexity: O(h), where h is the height of the recursion stack.
*/
