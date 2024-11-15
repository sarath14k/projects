#include <iostream>
#include <vector>
using namespace std;

struct Node{
    int val;
    Node * next;
    Node() : val(0), next(nullptr){}
    Node(int x) : val(x), next(nullptr){}
    Node(int x, Node* next) : val(x), next(next){}
};

Node * reverseList(Node* head){
    if(head == nullptr || head->next == nullptr)
        return head;

    Node* prev = nullptr;
    Node* curr = head;

    while(curr != nullptr){
        Node* temp = curr->next;
        curr->next = prev;
        prev = curr;
        curr = temp;
    }
    return prev;
}

void print(Node* head){
    while(head != nullptr){
        cout << head->val << " ";
        head = head->next;
    }
    cout << endl;
}

Node* createList(vector<int>& vals){
    Node* head = new Node(vals[0]);
    Node* current = head;
    for(int i = 1; i < vals.size(); i++){
        current->next = new Node(vals[i]);
        current = current->next;
    }
    return head;
}

int main()
{
    vector<int> values = {1,2,3,4,5};
    Node* head = createList(values);

    cout << "Orginal list => ";
    print(head);

    Node* revHead = reverseList(head);
    cout << "Reversed List =>";
    print(revHead);
}
