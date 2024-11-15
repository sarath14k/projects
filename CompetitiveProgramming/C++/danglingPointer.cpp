/*

A dangling pointer in C++ (or other languages that use pointers) is a pointer that continues to point to 
a memory location after that memory has been freed or deleted. Accessing a dangling pointer can lead to 
undefined behavior, as the memory it points to might be reallocated for other purposes, potentially 
causing program crashes or data corruption.

*/

int *ptr = new int(10);
delete ptr;    // ptr is now a dangling pointer
ptr = nullptr; // This prevents it from dangling

/*

How to Avoid Dangling Pointers:
1. Set pointers to nullptr after deletion to ensure that they are not used inadvertently.

2. Use smart pointers such as std::unique_ptr or std::shared_ptr, which automatically manage the
memory and prevent dangling pointers by ensuring that memory is only freed when it is no longer needed.

3. Be cautious with scope: Avoid returning pointers to local variables or accessing pointers after an
object's lifetime has ended.

*/