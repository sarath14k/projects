#ifndef API_CLIENT_H
#define API_CLIENT_H

#include <string>
#include <ctime> // Include for std::time_t

class APIClient {
public:
    APIClient(const std::string& apiKey, const std::string& apiSecret);
    
    std::string authenticate();
    std::string refreshAccessToken();
    std::string placeOrder(const std::string& instrumentName, double amount, const std::string& direction, const std::string& orderType, double price = 0.0);

private:
    std::string makeApiRequest(const std::string& endpoint, const std::string& payload, const std::string& method, const std::string& token = "");
    
    std::string apiKey;
    std::string apiSecret;
    std::string accessToken;
    std::string refreshToken;
    std::time_t tokenExpiry; // Ensure time_t is included
};

#endif // API_CLIENT_H
