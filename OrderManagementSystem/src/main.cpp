#include <iostream>
#include <vector>
#include "api_client.h"
#include "config_loader.h"

int main() {
    // Load your API credentials from a config file or hardcode for testing
    ConfigLoader config("config/config.yaml");
    APIClient client(config.getApiKey(), config.getApiSecret());

    std::vector<std::string> symbols = {"ETH-PERPETUAL"}; // Changed to ETH symbol for the example
    double orderAmount = 40.0; // Example order amount
    std::string orderType = "limit"; // Example order type
    double defaultPrice = 2000.0; // Example default price for limit order

    // Check which type of order to place
    std::string orderDirection = "buy"; // Example direction (buy/sell)

    // Place an order
    std::string response = client.placeOrder(symbols[0], orderAmount, orderDirection, orderType, defaultPrice);
    std::cout << "Order response: " << response << std::endl;

    return 0;
}
