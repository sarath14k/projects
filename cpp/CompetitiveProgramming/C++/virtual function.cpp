#include <iostream>
#include <string>

using namespace std;

class Vehicle
{
private:
    int model;

public:
    Vehicle(int m) : model(m) {}

    virtual void showDetails()
    {
        cout << "Below are the vehicle details" << endl;
    }

    int getModel()
    {
        return model;
    }

    virtual ~Vehicle() {}
};

class Car : public Vehicle
{
private:
    string color;

public:
    Car(int ml, const string &c) : Vehicle(ml), color(c) {}

    void showDetails() override
    {
        cout << "Model: " << getModel() << ", Color: " << color << endl;
    }
};

int main()
{
    //using Baseclass pointer
    Vehicle *v = new Car(1998, "Red"); // Base pointer pointing to Derived object
    v->showDetails();                  // Calls Derived's show function due to polymorphism

    delete v; // Free the allocated memory to avoid memory leaks
              // Correctly calls Derived and then Base destructors due to the virtual destructor
    return 0;
}

int main()
{
    // Using References 
    
    Car c(1998, "Red");
    Vehicle &v = c;
    v.showDetails(); // not pointer
                        // no need to delete 

    return 0;
}

// used virtual destructors when using base class pointers to point to derived class objects. 
// This ensures that derived class destructors are properly called during object destruction.