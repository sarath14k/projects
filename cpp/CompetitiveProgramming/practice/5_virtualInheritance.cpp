#include <iostream>
using namespace std;

// The grand-parent base class
class Device {
public:
    int id = 99; // Shared variable
};

// Virtual base classes prevent duplicate "Device" copies
class Camera : virtual public Device {};
class Phone  : virtual public Device {};

// The final derived class
class SmartPhone : public Camera, public Phone {};

int main() {
    SmartPhone myPhone;

    // WITHOUT 'virtual' above, this line throws a compile error: "id is ambiguous"
    // WITH 'virtual', there is only ONE unified copy of 'id'.
    cout << "Device ID: " << myPhone.id << endl; 

    return 0;
}
