#include <iostream>

class Node {
public:
    int data;       // Data stored in the node
    Node* next;     // Pointer to the next node

    Node(int val) : data(val), next(nullptr) {} // Constructor
};

class SinglyLinkedList {
private:
    Node* head; // Pointer to the head of the list

public:
    SinglyLinkedList() : head(nullptr) {} // Constructor

    // Insert a node at the end of the list
    void insert(int val) {
        Node* newNode = new Node(val);
        if (!head) {
            head = newNode; // If list is empty, new node is the head
            return;
        }
        
        Node* temp = head;
        while (temp->next) {
            temp = temp->next; // Traverse to the end of the list
        }
        temp->next = newNode; // Link the new node
    }

    // Display the list
    void display() const {
        Node* temp = head;
        while (temp) {
            std::cout << temp->data << " -> ";
            temp = temp->next;
        }
        std::cout << "nullptr" << std::endl;
    }

    // Destructor to free the memory
    ~SinglyLinkedList() {
        Node* temp = head;
        while (temp) {
            Node* next = temp->next;
            delete temp; // Delete the current node
            temp = next; // Move to the next node
        }
    }
};

int main() {
    SinglyLinkedList list;

    // Insert nodes
    list.insert(10);
    list.insert(20);
    list.insert(30);

    // Display the list
    std::cout << "Linked List: ";
    list.display();

    return 0;
}

// Delete a node by value
void deleteNode(int val) {
    if (!head) return; // If list is empty

    // If the head needs to be deleted
    if (head->data == val) {
        Node* temp = head;
        head = head->next; // Update head to the next node
        delete temp; // Delete the old head
        return;
    }

    Node* current = head;
    while (current->next && current->next->data != val) {
        current = current->next; // Traverse to find the node
    }

    if (current->next) {
        Node* temp = current->next;
        current->next = current->next->next; // Bypass the node to be deleted
        delete temp; // Delete the node
    }
}

// Search for a value in the list
bool search(int val) const {
    Node* temp = head;
    while (temp) {
        if (temp->data == val) {
            return true; // Value found
        }
        temp = temp->next;
    }
    return false; // Value not found
}

// Reverse the linked list
void reverse() {
    Node* prev = nullptr;
    Node* current = head;
    Node* next = nullptr;

    while (current) {
        next = current->next; // Store the next node
        current->next = prev; // Reverse the link
        prev = current; // Move prev and current one step forward
        current = next;
    }
    head = prev; // Update head to the new first node
}
