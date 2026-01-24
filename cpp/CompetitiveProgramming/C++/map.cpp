#include <iostream>
#include <map>

int main() {
    // Create a map of integers to strings
    std::map<int, std::string> myMap;

    // Insert elements into the map
    myMap[1] = "One";
    myMap[2] = "Two";
    myMap.insert(std::make_pair(3, "three"));

    // Display the elements of the map
    std::cout << "Map elements:" << std::endl;
    for (const auto& pair : myMap) {
        std::cout << "Key: " << pair.first << ", Value: " << pair.second << std::endl;
    }

    map<int, std::string>::iterator it;

    for (it = myMap.begin(); it != myMap.end(); ++it){
        cout << it->first << " -> " << it->second << endl;
    }

        // Accessing elements by key
        int key = 2;
    std::cout << "Value associated with key " << key << ": " << myMap[key] << std::endl;

    // Check if a key exists
    if (myMap.find(4) != myMap.end()) {
        std::cout << "Key 4 exists in the map." << std::endl;
    } else {
        std::cout << "Key 4 does not exist in the map." << std::endl;
    }

    return 0;

}
