#include <iostream>
#include <string>

using namespace std;

class Person {
private:
    string name;
    int age;

public:
    // Constructor
    Person(string n, int a) {
        name = n;
        age = a;
    }
    
    // Method to display person's information
    void displayInfo() {
        cout << "Name: " << name << endl;
        cout << "Age: " << age << endl;
    }

    // Declaring friend function
    friend void displayAge(Person p);
};

// Defining friend function
void displayAge(Person p) {
    // Accessing private member variable 'age' directly
    cout << "Friend function - Age: " << p.age << endl;
}

int main() {
    // Creating an object of class Person with constructor
    Person person1("John", 25);

    // Displaying information using the method
    person1.displayInfo();

    // Calling friend function to display age
    displayAge(person1);

    return 0;
}
