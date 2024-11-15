#include <bits/stdc++.h>
using namespace std;

struct Node {
    int val;
    Node* next;
    Node() : val(0), next(nullptr) {}
    Node(int x) : val(x), next(nullptr) {}
    Node(int x, Node* next) : val(x), next(next) {}
};

/** Reorder List */
class Solution {
public:
    void reorderList(Node* head) {
        // Step 1: Find the middle of the list using slow and fast pointers
        Node* slow = head;
        Node* fast = head->next;
        while (fast != nullptr && fast->next != nullptr) {
            slow = slow->next;
            fast = fast->next->next;
        }

        // Step 2: Reverse the second half of the list
        Node* second = slow->next;
        Node* prev = slow->next = nullptr;  // Disconnect the first half from the second
        while (second != nullptr) {
            Node* tmp = second->next;
            second->next = prev;
            prev = second;
            second = tmp;
        }

        // Step 3: Merge the two halves (first half and reversed second half)
        Node* first = head;
        second = prev;  // second now points to the head of the reversed list
        while (second != nullptr) {
            Node* tmp1 = first->next;
            Node* tmp2 = second->next;
            first->next = second;  // Insert node from second half
            second->next = tmp1;  // Connect to the next node from first half
            first = tmp1;
            second = tmp2;
        }
    }
    /*
    Time Complexity: O(n), where n is the number of nodes in the linked list.
    Space Complexity: O(1), since the reordering is done in place.
    */
};

// Helper function to print the list
void printList(Node* head) {
    while (head != nullptr) {
        cout << head->val << " ";
        head = head->next;
    }
    cout << endl;
}

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

int main() {
    Solution solution;

    // Create a linked list from a vector of values
    vector<int> list_values = {1, 2, 3, 4, 5};
    Node* head = createList(list_values);

    // Print the original list
    cout << "Original List: ";
    printList(head);

    // Reorder the list
    solution.reorderList(head);

    // Print the reordered list
    cout << "Reordered List: ";
    printList(head);

    return 0;
}
