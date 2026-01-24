#include <iostream>
#include <set>
#include <unordered_set>

void set(){
    std::set<int> mySet;

    mySet.insert(10);
    mySet.insert(20);
    mySet.insert(10); // Duplicate value, will not be inserted

    // Display the elements of the set
    std::cout << "Set elements: ";
    for (int num : mySet) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
}

void unorderedSet(){
    std::unordered_set<int> myUnorderedSet;

    myUnorderedSet.insert(10);
    myUnorderedSet.insert(20);
    myUnorderedSet.insert(10); // Duplicate value, will not be inserted

    // Display the elements of the unordered set
    std::cout << "Unordered set elements: ";
    for (int num : myUnorderedSet) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
}

int main() {
    
    set();
    unorderedSet();
    return 0;
}
