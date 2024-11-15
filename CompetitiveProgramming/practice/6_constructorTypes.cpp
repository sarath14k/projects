#include <iostream>
#include <cstring>
#include <utility>

using namespace std;

class FileManager
{
    private:
        char* data;
        size_t size;
    public:
        // Default
        FileManager() : data(nullptr), size(0)
        {
            cout << "Default called\n";
        }

        // Parameterized
        FileManager(const char* fileData) 
        {
            cout << "Parameterized called\n";
            size = strlen(fileData);
            data = new char[size + 1];
            strcpy(data, fileData);
        }

        //Copy
        FileManager(const FileManager& other)
        {
            cout << "Copy called\n";
            size = other.size;
            if(size > 0)
            {
                data = new char[size + 1];
                strcpy(data, other.data);
            } else
                data = nullptr;
        }

        // Move
        FileManager(FileManager&& other) noexcept : data(other.data), size(other.size)
        {
            cout << "Move called\n";
            other.data = nullptr;
            other.size = 0;
        }

        //Move Assignment operator
        FileManager& operator=(FileManager&& other) noexcept
        {
            cout << "Move assignment operator called\n";
            if(this != &other)//Avoid self assignment 
            {
                delete[] data; // Free current data
                data = other.data;
                size = other.size;

                other.data = nullptr; //Leave other in a valid state;
                other.size = 0;
            }
            return *this;
        }

        // Destructor
        ~FileManager()
        {
            cout << "Destructor called\n";
            delete[] data; // Free allocated memory
        }

        // Display file data
        void display() const
        {
            if (data)
                cout << "Data => " << data << '\n';
            else
                cout << "No data found\n";
        }
};

int main() {
    // Using default
    FileManager file1;
    file1.display();

    // Using param
    FileManager file2("Hello, FileManager!");
    file2.display();

    // Using copy
    FileManager file3 = file2;
    file3.display();

    // Using move
    FileManager file4 = move(file2); // File2 is a temp rvalue
    file4.display();
    file2.display(); // now empty

    // Using move assignment operator
    file1 = move(file4); // move data from file4 to file1
    file1.display();
    file4.display();

    return 0;
}
