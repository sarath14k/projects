#include <iostream>
#include <string>
using namespace std;

class Person {
private:
    string name;

public:
    // Constructor to initialize name
    Person(const string& name) : name(name) {}

    // Function to set the person's name
    void setName(const string& name) {
        this->name = name;  // 'this->name' refers to the member, 'name' refers to the parameter
    }

    // Function to display the person's name
    void display() const {
        cout << "Name: " << this->name << endl;
    }
};

int main() {
    Person person("John");
    person.display();

    person.setName("Alice");  // Update name using setName
    person.display();

    return 0;
}

