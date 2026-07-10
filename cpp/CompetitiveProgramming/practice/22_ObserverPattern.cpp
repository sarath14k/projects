#include <iostream>
#include <vector>

/**
 * WHAT IT IS: 
 * The interface for the "Subscriber". 
 * * WHY IT'S USEFUL: 
 * It allows objects to receive updates automatically without 
 * having to constantly check or ask (eliminates wasteful polling).
 */
struct Observer { 
    virtual void notify() = 0; 
};

/**
 * SPECIALITY: Loose Coupling
 * The data sender (Subject) doesn't know details about 'User'. 
 * It only cares that 'User' implements the Observer interface.
 */
struct User : Observer { 
    void notify() override { std::cout << "User received alert!\n"; } 
};

/**
 * WHAT IT IS: 
 * The "Publisher" or "Subject". It owns the state/data.
 * * WHY IT'S USEFUL: 
 * Manages a one-to-many relationship. One broadcast alerts infinite listeners.
 */
struct Subject {
    // SPECIALITY: Dynamic Relationships
    // Listeners can attach or detach themselves freely at runtime.
    std::vector<Observer*> subs; 
    
    void add(Observer* o) { subs.push_back(o); }
    
    // Broadcast method to push events down to all subscribers.
    void alert() { 
        for(auto s : subs) s->notify(); 
    }
};

int main() {
    Subject channel;
    User alice;
    
    channel.add(&alice); // Alice signs up
    channel.alert();     // Fires the event to everyone on the list
}
