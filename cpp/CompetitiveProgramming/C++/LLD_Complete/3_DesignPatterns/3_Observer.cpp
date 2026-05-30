// To compile and run: cd /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/3_DesignPatterns && g++ -std=c++17 3_Observer.cpp -o 3_Observer && ./3_Observer
#include <iostream>
#include <vector>

/*
 * CONCEPT: Observer Design Pattern
 * 
 * WHAT: A behavioral pattern that defines a one-to-many dependency. When one object 
 *       (Subject) changes state, all its dependents (Observers) are notified automatically.
 * 
 * HOW: The Subject holds a list of Observer pointers. When the Subject's state changes, 
 *      it loops through the list and calls an `update()` method on each Observer.
 * 
 * WHY: Highly decouples systems. The Subject doesn't need to know anything about the Observers 
 *      other than that they implement `update()`. Excellent for event systems, UI updates, or publish/subscribe.
 */

class Observer { 
public: 
    virtual void update() = 0; 
    virtual ~Observer(){} 
};

class Subject {
    std::vector<Observer*> obs;
public:
    void add(Observer* o) { 
        obs.push_back(o); 
    }
    
    void notify() { 
        for(auto o : obs) {
            o->update(); 
        }
    }
};

class User : public Observer { 
public: 
    void update() override { 
        std::cout << "User was notified of a change!\n"; 
    } 
};

int main() { 
    Subject s; 
    User u; 
    
    s.add(&u); 
    s.notify(); // Automatically triggers u.update()
    
    return 0; 
}
