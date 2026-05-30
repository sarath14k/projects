// To compile and run: cd /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/5_Modern_CPP && g++ -std=c++17 2_RAII.cpp -o 2_RAII && ./2_RAII
#include <iostream>
#include <fstream>

/*
 * CONCEPT: RAII (Resource Acquisition Is Initialization)
 * 
 * WHAT: A C++ programming idiom where the lifespan of a resource (like memory, file handles, 
 *       or network sockets) is tied to the lifespan of a local object.
 * 
 * HOW: Acquire the resource in the object's constructor, and release the resource in the 
 *      object's destructor.
 * 
 * WHY: When an object goes out of scope (even due to an exception), C++ guarantees its 
 *      destructor is called. This guarantees the resource is released safely, preventing leaks.
 */

class FileHandler {
private:
    std::ofstream file;
public:
    // Resource Acquired in Initialization (Constructor)
    FileHandler(const std::string& filename) {
        file.open(filename);
        if (file.is_open()) {
            std::cout << "File opened successfully.\n";
        }
    }
    
    void write(const std::string& data) {
        if (file.is_open()) {
            file << data << "\n";
            std::cout << "Wrote to file.\n";
        }
    }

    // Resource Released automatically in Destructor
    ~FileHandler() {
        if (file.is_open()) {
            file.close();
            std::cout << "File closed safely.\n";
        }
    }
};

int main() {
    {
        FileHandler fh("test_raii.txt");
        fh.write("RAII is awesome!");
    } // fh goes out of scope here, file is automatically closed!
    
    return 0;
}
