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
    /**
     * Function to detect if a cycle exists in the linked list.
     * @param head: Pointer to the head of the linked list.
     * @return: True if a cycle is found, otherwise false.
     */
    bool hasCycle(Node* head) {
        // Initialize two pointers: fast and slow
        Node* fast = head;
        Node* slow = head;

        // Traverse the list
        while (fast != nullptr && fast->next != nullptr) {
            fast = fast->next->next;  // Fast pointer moves 2 steps
            slow = slow->next;        // Slow pointer moves 1 step

            // If they meet, there's a cycle
            if (fast == slow) {
                return true;
            }
        }

        return false;  // No cycle found
    }

    /*
    Time Complexity: O(n), where n is the number of nodes in the linked list.
    Space Complexity: O(1), because we only use two pointers.
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

// Function to create a cycle in the list for testing purposes
void createCycle(Node* head, int pos) {
    if (pos < 0) return;

    Node* tail = head;
    Node* cycleStart = nullptr;
    int index = 0;

    while (tail->next != nullptr) {
        if (index == pos) {
            cycleStart = tail;
        }
        tail = tail->next;
        index++;
    }

    // Connect the last node to the node at position `pos`
    if (cycleStart != nullptr) {
        tail->next = cycleStart;
    }
}

int main() {
    Solution solution;

    // Create a linked list
    vector<int> list_values = {3, 2, 0, -4};
    Node* head = createList(list_values);

    // Create a cycle: position 1 means the cycle starts at value 2
    createCycle(head, 1);

    // Check if the list has a cycle
    bool result = solution.hasCycle(head);
    cout << "Does the linked list have a cycle? " << (result ? "Yes" : "No") << endl;

    return 0;
}
