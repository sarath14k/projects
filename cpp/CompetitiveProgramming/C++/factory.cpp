/* 
FACTORY METHOD PATTERN
Definition: Defines an interface for creating an object, but lets subclasses decide which class to instantiate.
Use Case: When a system needs to be independent of how its products are created.
*/
#include <iostream>
#include <memory>
#include <string>

// Product Interface
class Toy {
public:
    virtual void play() = 0;
    virtual ~Toy() {}
};

// Concrete Product A
class Car : public Toy {
public:
    void play() override { std::cout << "Driving the toy car! Vroom!" << std::endl; }
};

// Concrete Product B
class Robot : public Toy {
public:
    void play() override { std::cout << "Robot is walking! Beep Boop!" << std::endl; }
};

// Factory Class
class ToyFactory {
public:
    // Factory Method: Returns a smart pointer to a new object
    static std::unique_ptr<Toy> createToy(const std::string& type) {
        if (type == "car") return std::make_unique<Car>();
        if (type == "robot") return std::make_unique<Robot>();
        return nullptr;
    }
};

int main() {
  std::cout << "--- Factory Method Pattern ---" << std::endl;

  // We ask the factory for a "robot", and it gives us the right object.
  // We don't need to know the 'Robot' class exists.
  std::unique_ptr<Toy> myToy = ToyFactory::createToy("robot");
  
  if (myToy) {
    myToy->play();
  }

  return 0;
}
