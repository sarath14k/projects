#include <iostream>
using namespace std;

/*
 * ============================================================================
 * DESIGN PATTERN: SINGLETON
 * ============================================================================
 * PURPOSE:
 * Ensures that a class has exactly ONE instance globally across the entire 
 * program lifecycle and provides a single, global access point to it.
 *
 * KEY STRUCTURAL POINTS:
 * 1. Private Constructor: Prevents direct allocation using the 'new' keyword.
 * 2. Deleted Copy/Assignment: Prevents cloning or copying the unique instance.
 * 3. Static Instance Method: Manages the single lifecycle and returns it safely.
 * ============================================================================
 */

class DatabaseConnection {
private:
    // POINT 1: Hide the constructor so no one can execute 'new DatabaseConnection()'
    DatabaseConnection() { cout << "Connected to Database!\n"; }

public:
    // POINT 2: Remove copy mechanics so copies can never accidentally be created
    DatabaseConnection(const DatabaseConnection&) = delete;
    DatabaseConnection& operator=(const DatabaseConnection&) = delete;

    // POINT 3: Provide a global access function using Meyers' Singleton approach.
    // This instance is lazily initialized on the very first call and is thread-safe.
    static DatabaseConnection& getInstance() {
        static DatabaseConnection instance; 
        return instance;
    }

    void query(const string& sql) {
        cout << "Executing: " << sql << "\n";
    }
};

int main() {
    // Both calls interact with the exact same block of memory behind the scenes
    DatabaseConnection::getInstance().query("SELECT * FROM users");
    DatabaseConnection::getInstance().query("SELECT * FROM products");
    return 0;
}
