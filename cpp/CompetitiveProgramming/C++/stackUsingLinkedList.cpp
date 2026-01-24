#include <iostream>
using namespace std;

class Node
{

public:
    int data;
    Node *next;
    Node(int value) : data(value), next(nullptr) {}
};

class Stack
{

private:
    Node *head;

public:
    Stack() : head(nullptr) {}

    void push(int value)
    {

        Node *newNode = new Node(value);
        newNode->next = head;
        head = newNode;
    }

    void showStack()
    {

        if (head == nullptr)
        {
            cout << "empty stack" << endl;
        }
        else
        {

            Node *current = head;
            while (current != nullptr)
            {

                cout << current->data << endl;
                current = current->next;
            }
        }
    }

    void pop()
    {
        if (head == nullptr)
        {
            cout << "empty Stack- unable to pop" << endl;
        }
        else
        {
            Node *current = head;
            cout << "popped - " << current->data << endl;
            head = current->next;
            delete current;
        }
    }
};

int main()
{
    Stack s;
    s.push(50);
    s.push(40);
    s.push(30);
    s.showStack();
    s.pop();
    s.showStack();
    s.push(20);
    cout << " ----- " << endl;
    s.showStack();

    s.pop();
    s.pop();

    cout << " ----- " << endl;
    s.showStack();

    s.pop();
    cout << " ----- " << endl;
    s.showStack();

    s.pop();

    return 0;
}




