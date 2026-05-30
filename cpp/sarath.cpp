#include <iostream>
#include <string>

/*
 * FACTORIAL RECURSIVE TREE VISUALIZATION
 * 
 * This explicitly draws the nodes and shows the exact values held 
 * inside the current node BEFORE and AFTER the recursive call finishes.
 */

int factorial(int n, int depth = 0) {
    std::string indent(depth * 7, ' ');
    
    // Draw the arrow connecting the parent to this child node
    if (depth > 0) {
        std::cout << indent.substr(0, depth*7 - 3) << "|\n";
        std::cout << indent.substr(0, depth*7 - 3) << "V\n";
    }
    
    // ----------------- NODE ENTRY (Going down) -----------------
    std::cout << indent << "[Node: fact(" << n << ")]\n";

    // Base Case
    if (n <= 1) {
        std::cout << indent << "    |-- Base Case Reached!\n";
        std::cout << indent << "    |-- Value of n: " << n << "\n";
        std::cout << indent << "    |-- I return: 1\n";
        return 1;
    }

    // Recursive Step
    // The node pauses here and waits for the child to finish!
    int child_result = factorial(n - 1, depth + 1);

    // ----------------- NODE EXIT (Unwinding back up) -----------
    int my_result = n * child_result;
    
    std::cout << indent.substr(0, depth*7 + 3) << "^\n";
    std::cout << indent.substr(0, depth*7 + 3) << "|\n";
    std::cout << indent << "[Back inside Node: fact(" << n << ")]\n";
    std::cout << indent << "    |-- Value of n: " << n << "\n";
    std::cout << indent << "    |-- Child fact(" << n-1 << ") returned: " << child_result << "\n";
    std::cout << indent << "    |-- I calculate: " << n << " * " << child_result << " = " << my_result << "\n";
    std::cout << indent << "    |-- I return: " << my_result << "\n";

    return my_result;
}

int main() {
    std::cout << "--- Explicit Factorial Node Values (N = 4) ---\n\n";
    
    int final_answer = factorial(4);
    
    std::cout << "\nFinal Answer: " << final_answer << "\n";
    
    return 0;
}
