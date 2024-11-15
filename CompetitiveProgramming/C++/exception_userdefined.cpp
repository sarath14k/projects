#include <iostream>
#include <exception>
#include <string>

class MyException : public std::exception
{
public:
    MyException(const std::string &message) : msg(message) {}

    virtual const char *what() const noexcept override
    {
        return msg.c_str();
    }

private:
    std::string msg;
};

int main()
{
    try
    {
        // Throw the user-defined exception
        throw MyException("This is a user-defined exception!");
    }
    catch (const MyException &e)
    {
        // Catch and handle the user-defined exception
        std::cout << "Caught exception: " << e.what() << std::endl;
    }

    return 0;
}
