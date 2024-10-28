#include <bits/stdc++.h>
using namespace std;

/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */

struct ListNode {
    int val;
    ListNode* next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode* next) : val(x), next(next) {}
};

class Solution {
public:
    // Function to reverse the linked list
    ListNode* reverseList(ListNode* head) {
        if (head == nullptr || head->next == nullptr)  // Base case: Empty list or single node
            return head;

        ListNode* prev = nullptr;  // Initialize the previous pointer to null
        ListNode* curr = head;     // Start with the head of the list

        while (curr != nullptr) {
            ListNode* temp = curr->next;  // Temporarily store the next node
            curr->next = prev;            // Reverse the current node's pointer
            prev = curr;                  // Move prev forward
            curr = temp;                  // Move curr forward
        }
        return prev;  // The new head of the reversed list
    }
    /*
    Time Complexity: O(n), where n is the number of nodes in the list.
    Space Complexity: O(1), only a few pointers are used for the reversal process.
    */
};

// Helper function to print the list
void printList(ListNode* head) {
    while (head != nullptr) {
        cout << head->val << " ";
        head = head->next;
    }
    cout << endl;
}

// Helper function to create a linked list from an array of values
ListNode* createList(vector<int> vals) {
    ListNode* head = new ListNode(vals[0]);
    ListNode* current = head;

    for (int i = 1; i < vals.size(); i++) {
        current->next = new ListNode(vals[i]);
        current = current->next;
    }

    return head;
}

int main() {
    Solution solution;

    // Create a linked list: 1 -> 2 -> 3 -> 4 -> 5
    vector<int> values = {1, 2, 3, 4, 5};
    ListNode* head = createList(values);
    
    cout << "Original List: ";
    printList(head);  // Print original list
    
    // Reverse the list
    ListNode* reversedHead = solution.reverseList(head);

    // Output the reversed list
    cout << "Reversed List: ";
    printList(reversedHead);

    return 0;
}
