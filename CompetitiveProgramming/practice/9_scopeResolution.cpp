#include <iostream>
#include <string>

// Global variable with the same name as a class static variable
double interestRate = 3.5;

// Global function
void displayGlobalInterestRate() {
    std::cout << "Global Interest Rate: " << interestRate << "%\n";
}

class BankAccount {
private:
    std::string accountHolder;
    double balance;
    static double interestRate; // Static member variable

public:
    BankAccount(const std::string& holder, double bal) 
        : accountHolder(holder), balance(bal) {}

    // Member function to display account details
    void displayAccount() const {
        std::cout << "Account Holder: " << accountHolder << "\n";
        std::cout << "Balance: $" << balance << "\n";
        std::cout << "Account Interest Rate: " << interestRate << "%\n"; // Accessing static member
    }

    // Static function to set interest rate
    static void setInterestRate(double rate) {
        interestRate = rate;
    }

    // Friend function defined outside class using ::
    friend void displayAccountDetails(const BankAccount& account);
};

// Define static member outside the class using ::
double BankAccount::interestRate = 2.5;

// Friend function defined outside the class using ::
void displayAccountDetails(const BankAccount& account) {
    std::cout << "Friend Function - Accessing Account Holder: " << account.accountHolder << "\n";
    std::cout << "Balance from Friend Function: $" << account.balance << "\n";
}

int main() {
    // Access global function and variable
    ::displayGlobalInterestRate();
    std::cout << "Accessing global interest rate variable directly: " << ::interestRate << "%\n\n";

    // Create BankAccount object
    BankAccount account("John Doe", 1000);

    // Use class member and static member
    account.displayAccount();

    // Update interest rate using static function
    BankAccount::setInterestRate(4.0);

    std::cout << "\nAfter updating interest rate:\n";
    account.displayAccount();

    // Access friend function defined outside the class
    displayAccountDetails(account);

    return 0;
}

