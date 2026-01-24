#include <iostream>
#include <string>
using namespace std;

class Person
{
    private:
        string ssn; // accessible within class and with the use of friend
    protected:
        string name; // Accessible in derived classes;
    public:
        int age; // accessible anywhere
        Person(const string& n, int a, const string& s)
              : name(n), age(a), ssn(s) {}
        friend void displayPerson(const Person& person);
        friend class HR;
        
};

void displayPerson(const Person& person)
{
    cout << "Person's SSN (Private) : " << person.ssn << "\n";
}

// Friend class
class HR
{
    public:
        void viewSSN(const Person& person)
        {
            // accessing private members of person
            cout << "HR viewing SSN : " << person.ssn << '\n';
        }
};

// Employee inherits from Person publically
class Employee : public Person
{
    public:
        string department;
        Employee(const string& n, int a, const string& s, const string& dept)
                : Person(n, a, s), department(dept) {}
        void displayEmployee() {
            cout << "Employee Name (Protected): " << name << "\n";
            cout << "Employee Age (Public): " << age << "\n";
            cout << "Department (Public): " << department << "\n";
        }
};

// Manager inherits from Employee with protected inheritance 
class Manager : protected Employee 
{
    public:
        Manager(const string& n, int a, const string& s, const string& dept)
                : Employee(n, a, s, dept) {}
        
        void displayManager()
        {
            cout << "Manager Name (Protected Inheritance) : " << name << '\n';
            cout << "Manager Age (Protected Inheritance) : " << age << '\n';
            cout << "Department (Protected Inheritance) : " << department<< '\n';
        }
};

// Executive inherits from Manager with private inheritance
class Executive : private Manager
{
    public:
        Executive(const string& n, int a, const string& s, const string& dept)
                : Manager(n, a, s, dept) {}
        
        void displayExecutive()
        {
            cout << "Executive details(Private inh - Name, Age, Dept) :\n";
            displayManager();
        }
};

int main() {
    Person person("Alice", 30, "123-45-6789");
    Employee employee("Bob", 40, "987-65-4321", "Finance");
    Manager manager("Charlie", 50, "567-89-1234", "Operations");
    Executive executive("Dana", 60, "345-67-8901", "Executive");

    cout << "Accessing public member directly:\n";
    cout << "Person Age: " << person.age << "\n\n";

    cout << "Accessing through public inheritance (Employee):\n";
    employee.displayEmployee();
    cout << "\n";

    cout << "Accessing through protected inheritance (Manager):\n";
    manager.displayManager();
    cout << "\n";

    cout << "Accessing through private inheritance (Executive):\n";
    executive.displayExecutive();
    cout << "\n";

    cout << "Accessing private member through friend function:\n";
    displayPerson(person);
    cout << "\n";

    cout << "Accessing private member through friend class:\n";
    HR hr;
    hr.viewSSN(person);

    return 0;
}
