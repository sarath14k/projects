#include <iostream>
#include "deribit_api.h"

int main() {
    DeribitAPI api;

    while (true) {
        std::cout << "Select an option:\n";
        std::cout << "1. Place Order\n";
        std::cout << "2. Cancel Order\n";
        std::cout << "3. Modify Order\n";
        std::cout << "4. Get Orderbook\n";
        std::cout << "5. View Current Positions\n";
        std::cout << "6. Exit\n";
        std::cout << "Enter your choice: ";

        int choice;
        std::cin >> choice;

        switch (choice) {
            case 1: {
                double amount, price;
                std::string instrument_name, order_type;
                std::cout << "Enter amount: ";
                std::cin >> amount;
                std::cout << "Enter instrument name (e.g., ETH-PERPETUAL): ";
                std::cin >> instrument_name;
                std::cout << "Enter order type (e.g., market): ";
                std::cin >> order_type;
                if(order_type != "market")
                    price = 2000;
                


                std::string response = api.placeOrder(amount, instrument_name, order_type, price);
                std::cout << "Order Response: " << response << std::endl;
                break;
            }
            case 2: {
                std::string order_id;
                std::cout << "Enter order ID to cancel: ";
                std::cin >> order_id;
                std::string response = api.cancelOrder(order_id);
                std::cout << "Cancel Order Response: " << response << std::endl;
                break;
            }
            case 3: {
                std::string order_id;
                double amount, price;
                std::cout << "Enter order ID to modify: ";
                std::cin >> order_id;
                std::cout << "Enter new amount: ";
                std::cin >> amount;
                std::cout << "Enter new price: ";
                std::cin >> price;

                std::string response = api.modifyOrder(order_id, amount, price);
                std::cout << "Modify Order Response: " << response << std::endl;
                break;
            }
            case 4: {
                std::string instrument_name;
                int depth;
                std::cout << "Enter instrument name (e.g., BTC-PERPETUAL): ";
                std::cin >> instrument_name;
                std::cout << "Enter depth: ";
                std::cin >> depth;

                std::string response = api.getOrderBook(instrument_name, depth);
                std::cout << "Order Book Response: " << response << std::endl;
                break;
            }
            case 5: {
                std::string response = api.viewCurrentPositions();
                std::cout << "Current Positions Response: " << response << std::endl;
                break;
            }
            case 6:
                std::cout << "Exiting...\n";
                return 0;
            default:
                std::cout << "Invalid choice, please try again.\n";
        }

        std::cout << std::endl; 
    }

    return 0;
}
