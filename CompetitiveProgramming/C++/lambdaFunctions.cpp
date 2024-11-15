In C++, lambda functions (also known as anonymous functions) are functions defined at the point of use 
without having to declare them separately. 
Lambda functions are typically used for short snippets of code where defining a named function
would be overkill. They are often passed as arguments to algorithms or callback


[capture] (parameters) -> return_type
{
    body
}
------------------------------------------------

#include <iostream>
#include <vector>
#include <algorithm>

int main()
{
    // Example of a lambda function
    auto printMessage = []()
    {
        std::cout << "Hello, Lambda!" << std::endl;
    };

    // Call the lambda function
    printMessage();

    return 0;
}

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -

#include <iostream>

int main()                                       
{
    // Lambda function with parameters and explicit return type
    auto add = [](int x, int y) -> int
    {
        return x + y;
    };

    std::cout << "Sum: " << add(10, 20) << std::endl; // Output: Sum: 30

    return 0;
}

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#include <iostream>
#include <vector>
#include <algorithm>

int main()
{
    std::vector<int> numbers = {4, 2, 5, 3, 1};

    // Use lambda to sort in descending order
    std::sort(numbers.begin(), numbers.end(), [](int a, int b)
              {
                  return a > b; // Return true if 'a' is greater than 'b'
              });

    // Print the sorted numbers
    for (int num : numbers)
    {
        std::cout << num << " "; // Output: 5 4 3 2 1
    }

    return 0;
}
