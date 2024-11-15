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

/** Iterative Solution */
class Solution {
public:
    // Function to merge two sorted linked lists iteratively
    Node* mergeTwoLists(Node* list1, Node* list2) {
        Node dummy(0);  // Dummy node to act as the head of the merged list
        Node* node = &dummy;  // Pointer to traverse and build the merged list

        // Traverse both lists until one becomes empty
        while (list1 && list2) {
            // Append the smaller value node to the merged list
            if (list1->val < list2->val) {
                node->next = list1;
                list1 = list1->next;  // Move list1 forward
            } else {
                node->next = list2;
                list2 = list2->next;  // Move list2 forward
            }
            node = node->next;  // Move the merged list pointer forward
        }

        // Append any remaining nodes from either list1 or list2
        if (list1) {
            node->next = list1;
        } else {
            node->next = list2;
        }

        return dummy.next;  // Return the next node after dummy, which is the head of the merged list
    }
    /*
    Time Complexity: O(n + m), where n and m are the lengths of list1 and list2, respectively.
    Space Complexity: O(1), since we are only using a few pointers and not allocating extra space proportional to the input size.
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

    // Create two sorted linked lists
    vector<int> list1_values = {1, 3, 5};
    vector<int> list2_values = {2, 4, 6};

    Node* list1 = createList(list1_values);
    Node* list2 = createList(list2_values);

    // Print original lists
    cout << "List 1: ";
    printList(list1);

    cout << "List 2: ";
    printList(list2);

    // Merge the two lists
    Node* mergedList = solution.mergeTwoLists(list1, list2);

    // Print the merged list
    cout << "Merged List: ";
    printList(mergedList);

    return 0;
}
