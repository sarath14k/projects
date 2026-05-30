/* 
SINGLETON PATTERN
Definition: Ensures a class has only one instance and provides a global point of access to it.
Use Case: Database connections, Loggers, Thread pools, Configuration settings.
*/
#include <iostream>
#include <memory>
#include <string>

class Database {
public:
  // 1. Access point: Static method to get the single instance
  static Database &getInstance() {
    // C++11 guarantees this initialization is thread-safe!
    static Database instance;
    return instance;
  }

  void query(std::string sql) {
    std::cout << "Executing: " << sql << std::endl;
  }

  // 2. IMPORTANT: Remove the ability to copy or clone the instance
  // Database d2 = d1; -> Error
  Database(const Database &) = delete;

  // Database d2; d2 = d1; -> Error
  void operator=(const Database &) = delete;

private:
  // 3. Private constructor: Prevents creating objects outside the class using 'new Database()'
  Database() { std::cout << "Database Connection Opened." << std::endl; }
};

int main() {
  // --- Singleton Demo ---
  std::cout << "--- Singleton ---" << std::endl;
  
  // Database::getInstance() returns a reference to the static object.
  // We then immediately call .query() on that reference (Method Chaining).
  Database::getInstance().query("SELECT * FROM users");
  
  // We can also store the reference if we want to use it multiple times.
  Database &db = Database::getInstance();
  db.query("DROP TABLE bugs");

  return 0;
}
