#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode* next) : val(x), next(next) {}
};

/** Reorder List */
class Solution {
public:
    void reorderList(ListNode* head) {
        // Step 1: Find the middle of the list using slow and fast pointers
        ListNode* slow = head;
        ListNode* fast = head->next;
        while (fast != nullptr && fast->next != nullptr) {
            slow = slow->next;
            fast = fast->next->next;
        }

        // Step 2: Reverse the second half of the list
        ListNode* second = slow->next;
        ListNode* prev = slow->next = nullptr;  // Disconnect the first half from the second
        while (second != nullptr) {
            ListNode* tmp = second->next;
            second->next = prev;
            prev = second;
            second = tmp;
        }

        // Step 3: Merge the two halves (first half and reversed second half)
        ListNode* first = head;
        second = prev;  // second now points to the head of the reversed list
        while (second != nullptr) {
            ListNode* tmp1 = first->next;
            ListNode* tmp2 = second->next;
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
void printList(ListNode* head) {
    while (head != nullptr) {
        cout << head->val << " ";
        head = head->next;
    }
    cout << endl;
}

// Helper function to create a linked list from a vector of values
ListNode* createList(const vector<int>& values) {
    if (values.empty()) return nullptr;
    ListNode* head = new ListNode(values[0]);
    ListNode* current = head;

    for (int i = 1; i < values.size(); i++) {
        current->next = new ListNode(values[i]);
        current = current->next;
    }

    return head;
}

int main() {
    Solution solution;

    // Create a linked list from a vector of values
    vector<int> list_values = {1, 2, 3, 4, 5};
    ListNode* head = createList(list_values);

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
