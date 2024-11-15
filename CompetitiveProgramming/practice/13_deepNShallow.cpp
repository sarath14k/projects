#include <iostream>
#include <string>
using namespace std;

class Document {
private:
    string* note;

public:
    // Constructor
    Document(const string& text) : note(new string(text)) {}

    // Copy Constructor for Deep Copy
    Document(const Document& doc) : note(new string(*doc.note)) {}

    // Display function
    void display() const { cout << "Note: " << *note << "\n"; }

    // Destructor to free memory
    ~Document() { delete note; }
};

int main() {
    Document original("Original Note");

    Document deepCopy(original);  // Deep copy

    cout << "Original: "; original.display();
    cout << "Deep Copy: "; deepCopy.display();

    return 0;
}

