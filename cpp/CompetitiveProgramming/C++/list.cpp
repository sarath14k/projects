#include <iostream>
#include <list>

int main()
{
    // Create a list of integers
    std::list<int> myList;

    // Insert elements into the list
    myList.push_back(10);
    myList.push_back(20);
    myList.push_back(10); // Duplicate value
    myList.push_back(30);
    myList.push_back(20); // Duplicate value

    // Display the elements of the list
    std::cout << "List elements: ";
    for (int num : myList)
    {
        std::cout << num << " ";
    }

    if (myList.find(10) != myList.end())
    {
        std::cout << "10 is found in the list";
    }

    if (myList.size() > 0)
    {
        std::cout << "List is not empty";
        auto it = myList.begin();
        ++it;
        std::cout << "First element: " << *it << std::endl;
        myList.erase(it);
        
    }

    std::cout << std::endl;

    return 0;
}

a list refers to a doubly linked list which is part of the Standard Template Library(STL).
A doubly linked list is a sequence of elements, where each element(node) contains a reference 
to both the next and previous elements. 
This allows for efficient insertion and deletion of elements from any position in constant time.

- Efficient insertions and deletions at both ends (front and back) and anywhere in the middle.
- Does not allow direct access to elements by index like vectors or arrays.
- Each node points to both the previous and next nodes.

#include <iostream>
#include <list>

int main()
{
    // Create and initialize a list
    std::list<int> myList = {10, 20, 30, 40, 50};

    // Display the original list
    std::cout << "Original list: ";
    for (int val : myList)
    {
        std::cout << val << " "; // Output: 10 20 30 40 50
    }
    std::cout << std::endl;

    // Get an iterator to the first element
    std::list<int>::iterator it = myList.begin();

    // Advance the iterator to the second element
    std::advance(it, 1); // Moves the iterator to the second element (20)

    // Erase the second element
    myList.erase(it);

    // Display the updated list after removing the second element
    std::cout << "Updated list: ";
    for (int val : myList)
    {
        std::cout << val << " "; // Output: 10 30 40 50
    }
    std::cout << std::endl;

    return 0;
}

Array:

Size: Fixed at compile-time (cannot be resized).
Memory Layout: Elements are stored contiguously, making random access very fast (O(1) access time).
Insertion/Deletion: Inserting or deleting elements, especially in the middle, is slow (O(n)) 
because all elements need to be shifted.
Use Case: Best for fixed-size collections where performance and memory efficiency are critical.



Vector:

Size: Dynamic, and it resizes itself as needed.
Memory Layout: Also stores elements contiguously, so it offers fast random access (O(1) access time).
Insertion/Deletion: Fast insertion and deletion at the end (amortized O(1)) but slower in the middle or 
front (O(n)) due to shifting.
Use Case: Ideal for dynamically-sized collections where elements are frequently added or removed at the end.


List:

Size: Dynamic, can grow or shrink as needed.
Memory Layout: Elements are linked rather than contiguous, making random access slower (O(n)).
Insertion/Deletion: Efficient for insertion and deletion at any position (O(1) with an iterator), 
especially useful if modifications occur frequently at various positions.
Use Case: Suitable for cases where frequent insertions and deletions happen at multiple positions.
In summary, I’d choose:

array for fixed-size collections,
vector for dynamic-size collections with frequent access and occasional end insertions,
list for frequent modifications throughout the collection."
