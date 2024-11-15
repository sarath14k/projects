#include <bits/stdc++.h>
using namespace std;

/**
 * Definition for singly-linked list.
 * struct Node {
 *     int val;
 *     Node *next;
 *     Node() : val(0), next(nullptr) {}
 *     Node(int x) : val(x), next(nullptr) {}
 *     Node(int x, Node *next) : val(x), next(next) {}
 * };
 */

struct Node {
    int val;
    Node* next;
    Node() : val(0), next(nullptr) {}
    Node(int x) : val(x), next(nullptr) {}
    Node(int x, Node* next) : val(x), next(next) {}
};

class Solution {
public:
    Node* removeNthFromEnd(Node* head, int n) {
        // Create a dummy node pointing to the head to handle edge cases
        Node* dummy = new Node(0, head);
        Node* left = dummy;
        Node* right = head;

        // Move the right pointer n steps ahead
        while (n > 0) {
            right = right->next;
            n--;
        }

        // Move both pointers until right reaches the end
        while (right != nullptr) {
            left = left->next;
            right = right->next;
        }

        // Remove the nth node by adjusting pointers
        left->next = left->next->next;

        // Return the new head (dummy->next)
        return dummy->next;
    }

    /*
    Time Complexity: O(n), where n is the number of nodes in the list.
    Space Complexity: O(1), as the algorithm uses constant space.
    */
};

// Helper function to create a linked list from a vector of values
Node* createList(const vector<int>& values) {
    if (values.empty()) return nullptr;
    Node* head = new Node(values[0]);
    Node* current = head;

    for (int i = 1; i < values.size(); i++) {
        current->next = new Node(values[i]);
        current = current->next;
    }

    return head;
}

// Helper function to print the list
void printList(Node* head) {
    while (head != nullptr) {
        cout << head->val << " ";
        head = head->next;
    }
    cout << endl;
}

int main() {
    Solution solution;

    // Create a linked list from a vector of values
    vector<int> list_values = {1, 2, 3, 4, 5};
    Node* head = createList(list_values);

    // Print the original list
    cout << "Original List: ";
    printList(head);

    // Remove the 2nd node from the end
    head = solution.removeNthFromEnd(head, 2);

    // Print the updated list
    cout << "Updated List after removing 2nd node from end: ";
    printList(head);

    return 0;
}
