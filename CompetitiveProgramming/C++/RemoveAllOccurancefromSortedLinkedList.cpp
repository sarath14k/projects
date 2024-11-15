
#include <bits/stdc++.h>
using namespace std;

struct ListNode
{
    int data;
    ListNode *next;
    ListNode() : data(0), next(nullptr) {}
    ListNode(int x) : data(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : data(x), next(next) {}
};

ListNode *deleteDuplicates(ListNode *head)
{
    unordered_map<int, int> NodeMap;

    if (head == nullptr)
    {
        return nullptr;
    }

    ListNode *Current = head;
    while (Current != nullptr)
    {
        NodeMap[Current->data]++;
        Current = Current->next;
    }

    ListNode *dummy = new ListNode(0);
    ListNode *tail = dummy;
    Current = head;

    while (Current != nullptr)
    {

        if (NodeMap[Current->data] == 1)
        {
            tail->next = new ListNode(Current->data);
            tail = tail->next;
        }
        Current = Current->next;
    }

    head = dummy->next;
    delete dummy;
    return head;
}

/*  Optimised Code

ListNode *deleteDuplicates(ListNode *head)
{
    if (!head) return nullptr;

    unordered_map<int, int> countMap;
    ListNode *current = head;

    // Count occurrences of each value
    while (current != nullptr)
    {
        countMap[current->data]++;
        current = current->next;
    }

    // Create a dummy node to simplify removal of head node if necessary
    ListNode *dummy = new ListNode(0, head);
    ListNode *prev = dummy;
    current = head;

    // Remove duplicates
    while (current != nullptr)
    {
        if (countMap[current->data] > 1)
        {
            prev->next = current->next;
            delete current;
        }
        else
        {
            prev = current;
        }
        current = prev->next;
    }

    head = dummy->next;
    delete dummy;
    return head;
}

*/

void printList(ListNode *head)
{
    ListNode *current = head;
    while (current != nullptr)
    {
        std::cout << current->data << " ";
        current = current->next;
    }
    std::cout << std::endl;
}

int main()
{
    // Creating a sorted linked list 1 -> 2 -> 2 -> 3 -> 3 -> 4
    ListNode *head = new ListNode{1, nullptr};
    head->next = new ListNode{2, nullptr};
    head->next->next = new ListNode{2, nullptr};
    head->next->next->next = new ListNode{3, nullptr};
    head->next->next->next->next = new ListNode{3, nullptr};
    head->next->next->next->next->next = new ListNode{4, nullptr};

    std::cout << "Original list: ";
    printList(head);

    head = deleteDuplicates(head);

    std::cout << "List after removing duplicates: ";
    printList(head);

    //Original list: 1 2 2 3 3 4
    //List after removing duplicates: 1 2 3 4

    // Clean up memory
    while (head != nullptr)
    {
        ListNode *temp = head;
        head = head->next;
        delete temp;
    }

    return 0;
}