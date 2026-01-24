/******************************************************************************

Welcome to GDB Online.
GDB online is an online compiler and debugger tool for C, C++, Python, Java, PHP, Ruby, Perl,
C#, OCaml, VB, Swift, Pascal, Fortran, Haskell, Objective-C, Assembly, HTML, CSS, JS, SQLite, Prolog.
Code, Compile, Run and Debug online from anywhere in world.

*******************************************************************************/
#include <bits/stdc++.h>
using namespace std;

struct Node
{
    int data;
    Node *next;
};

Node *removeDuplicates(Node *head)
{
    if (head == nullptr)
        return nullptr;

    Node *current = head;

    while (current != nullptr && current->next != nullptr)
    {
        if (current->data == current->next->data)
        {
            Node *duplicate = current->next;
            current->next = current->next->next;
            delete duplicate; // Free memory of the duplicate node
        }
        else
        {
            current = current->next;
        }
    }

    return head;
}

void printList(Node *head)
{
    Node *current = head;
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
    Node *head = new Node{1, nullptr};
    head->next = new Node{2, nullptr};
    head->next->next = new Node{2, nullptr};
    head->next->next->next = new Node{3, nullptr};
    head->next->next->next->next = new Node{3, nullptr};
    head->next->next->next->next->next = new Node{4, nullptr};

    std::cout << "Original list: ";
    printList(head);

    head = removeDuplicates(head);

    std::cout << "List after removing duplicates: ";
    printList(head);

    //  original list
    // 1 2 2 3 3 4
    // list after removing duplicates
    // 1 2 3 4

    // Clean up memory
    while (head != nullptr)
    {
        Node *temp = head;
        head = head->next;
        delete temp;
    }

    return 0;
}