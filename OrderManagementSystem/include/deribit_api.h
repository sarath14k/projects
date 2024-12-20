#ifndef DERIBIT_API_H
#define DERIBIT_API_H

#include <string>
#include <nlohmann/json.hpp> // Include a JSON library like nlohmann/json
#include <curl/curl.h>
#include "config.h"
using namespace Config;

class DeribitAPI {
public:
    DeribitAPI();
    std::string authenticate();
    std::string placeOrder(double amount, const std::string& instrument_name, const std::string& order_type, double price = 0);
    std::string cancelOrder(const std::string& order_id);
    std::string modifyOrder(const std::string& order_id, double amount, double price); 
    std::string getOrderBook(const std::string& instrument_name, int depth); 
    std::string viewCurrentPositions();

private:
    std::string accessToken;
    void setAccessToken(const std::string& token);
    static size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp);
    std::string performRequest(const std::string& url, const std::string& data, const std::string& method);
};

#endif // DERIBIT_API_H
