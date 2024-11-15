#include <iostream>
#include <string>
using namespace std;

class Media{
    public:
        virtual void play() const {
            cout << "Playing media.." <<endl;
        }
        virtual ~Media() {}
};

class Audio : public Media{
    public:
        virtual void play() const override{
            cout << "Playing audio.." <<endl;
        }
        void adjustVolume(){
            cout << "Adjusting volume" << endl;
        }
};

int main()
{
    // Example of static cast convertion of int to double
    int intVal = 42;
    double doubleVal = static_cast<double>(intVal);
    cout << "Double value(static cast): " << doubleVal << endl;

    // Example of dynamic cast : safe downcasting
    Media* media = new Audio();
    if(Audio* audio = dynamic_cast<Audio*>(media))
        audio->adjustVolume();

    // Example of const cast: removing const qualifier
    const int constVal = 10;
    int& nonConstVal = const_cast<int&>(constVal);
    nonConstVal = 20;
    cout << "Modified value(const cast): " << nonConstVal << endl;

    // Example of reinterpret_cast : converting pointer types
    int num = 5;
    int* numPtr = &num;
    char* charPtr = reinterpret_cast<char*>(numPtr);
    cout << "Address interpreted as char* (reinterpret_cast): "
        << static_cast<void*>(charPtr) << endl;
    delete media;
    return 0;
}

/*
 Explanation of Each Type Cast:

    static_cast:
        Converts intVal (an int) to doubleVal (a double). This is a safe cast for related types.

    dynamic_cast:
        Attempts to cast Media* to Audio*. If the object pointed to by media is actually an Audio, the cast succeeds, allowing access to adjustVolume. If the cast fails, audio will be nullptr, preventing access to invalid members.

    const_cast:
        Removes the const qualifier from constValue, allowing nonConstValue to be modified. Use this cautiously, as modifying const data can lead to undefined behavior.

    reinterpret_cast:
        Converts int* to char*, allowing the same address to be interpreted as a char pointer. This cast does not alter the data but treats it as a different type, mainly for low-level operations.
        */
