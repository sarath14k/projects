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
    // Function to check if two binary trees are the same
    bool isSameTree(TreeNode* p, TreeNode* q) {
        if (!p && !q) {
            return true; // Both nodes are null, trees are the same
        }
        if (p && q && p->val == q->val) {
            // Recursively check left and right subtrees
            return isSameTree(p->left, q->left) && isSameTree(p->right, q->right);
        } else {
            return false; // One of the nodes is null or values are different
        }
    }
};

int main() {
    // Create first tree: 
    //        1
    //       / \
    //      2   3
    TreeNode* tree1 = new TreeNode(1);
    tree1->left = new TreeNode(2);
    tree1->right = new TreeNode(3);

    // Create second tree:
    //        1
    //       / \
    //      2   3
    TreeNode* tree2 = new TreeNode(1);
    tree2->left = new TreeNode(2);
    tree2->right = new TreeNode(3);

    Solution solution;
    bool result = solution.isSameTree(tree1, tree2); // Check if both trees are the same

    cout << "Are the two trees the same? " << (result ? "Yes" : "No") << endl; // Print result

    return 0; // Return 0 to indicate successful execution
}

/*
Time Complexity: O(n), where n is the number of nodes in the trees (traversing both trees).
Space Complexity: O(h), where h is the height of the trees due to the recursive call stack.
*/
