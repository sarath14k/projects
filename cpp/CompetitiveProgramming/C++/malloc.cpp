//malloc
int *p = (int *)malloc(sizeof(int)); // Allocates memory but doesn't initialize          
free(p); // Deallocates memory, no destructors called

class MyClass
{
public:
    MyClass() { cout << "Constructor called" << endl; }
};

MyClass *obj = (MyClass *)malloc(sizeof(MyClass)); // Constructor not called


//new
int *p = new int; // Allocates memory and initializes (default initialization)
delete p; // Deallocates memory and calls destructors

MyClass *obj = new MyClass(); // Constructor called
