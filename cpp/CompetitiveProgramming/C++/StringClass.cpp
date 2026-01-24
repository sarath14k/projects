#include <iostream>
#include <cstring> // For strlen, strcpy
using namespace std;

class String  
{
private:
    char *buff;
    unsigned int len;

public:
    String() : buff(nullptr), len(0) {} //initializer list

    String(const char *msg)
    {
        len = strlen(msg);
        buff = new char[len + 1];
        strcpy(buff, msg);
    }

    // Copy constructor
    String(const String &other)
    {
        len = other.len;
        buff = new char[len + 1];
        strcpy(buff, other.buff);
    }

    // Copy assignment operator
    String &operator=(const String &other)
    {
        if (this != &other)
        {
            delete[] buff;
            len = other.len;
            buff = new char[len + 1];
            strcpy(buff, other.buff);
        }
        return *this;
    }

    // Move constructor
    String(String &&other) noexcept
    {
        len = other.len;
        buff = other.buff;
        other.buff = nullptr; // Nullify the other's buffer pointer
        other.len = 0;
    }

    // Move assignment operator
    String &operator=(String &&other) noexcept
    {
        if (this != &other)
        {
            delete[] buff;
            len = other.len;
            buff = other.buff;
            other.buff = nullptr; // Nullify the other's buffer pointer
            other.len = 0;
        }
        return *this;
    }

    // Destructor
    ~String()
    {
        delete[] buff;
    }

    unsigned int length() const
    {
        return len;
    }

    friend std::ostream &operator<<(std::ostream &os, const String &str);
    friend std::istream &operator>>(std::istream &is, String &str);
};

// Overloading << operator for output
std::ostream &operator<<(std::ostream &os, const String &str)
{
    if (str.buff)
    {
        os << str.buff;
    }
    return os;
}

// Overloading >> operator for input
std::istream &operator>>(std::istream &is, String &str)
{
    char temp[1000]; // Temporary buffer (adjust size as needed)
    is >> temp;

    // Clean up existing buffer
    delete[] str.buff;

    // Allocate new buffer and copy input
    str.len = strlen(temp);
    str.buff = new char[str.len + 1];
    strcpy(str.buff, temp);

    return is;
}

int main()
{
    String str1;        // Default constructor
    String str2("hai"); // Parameterized constructor
    String str3 = str1; // Copy constructor
    str3 = str2;        // Copy assignment operator
    int length = str3.length();
    String str4 = std::move(str2); // Move constructor

    cout << str4 << endl; // Overload <<
    cin >> str1;          // Overload >>
    cout << str1 << endl;
    return 0;
}
