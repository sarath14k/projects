
#include <iostream>
#include <string>
using namespace std;

class Toy {
protected:
  string name;
  float price;

public:
  virtual void prepareParts() {
    cout << "Preparing " << name << " parts" << endl;
  }
  virtual void combineParts() {
    cout << "Combining " << name << " parts" << endl;
  }
  virtual void assembleParts() {
    cout << "Assembling " << name << " parts" << endl;
  }
  virtual void applyLabel() { cout << "Applying " << name << " label" << endl; }
  virtual void showProduct() {
    cout << "Name: " << name << " | Price: " << price << endl;
  }
  virtual ~Toy() {}
};

class Car : public Toy {
public:
  Car() {
    name = "Car";
    price = 10.0;
  }
};

class Bike : public Toy {
public:
  Bike() {
    name = "Bike";
    price = 5.0;
  }
};

class Plane : public Toy {
public:
  Plane() {
    name = "Plane";
    price = 50.0;
  }
};
