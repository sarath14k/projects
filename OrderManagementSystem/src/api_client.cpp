#include "api_client.h"
#include <curl/curl.h>
#include <nlohmann/json.hpp>
#include <iostream>
#include <chrono>
#include <sstream> // Added for std::ostringstream

APIClient::APIClient(const std::string& apiKey, const std::string& apiSecret)
    : apiKey(apiKey), apiSecret(apiSecret), accessToken(""), refreshToken(""), tokenExpiry(0) {
    authenticate();  // Authenticate on initialization
}

std::string APIClient::authenticate() {
    std::string endpoint = "https://test.deribit.com/api/v2/public/auth";
    std::ostringstream payloadStream;
    payloadStream << "client_id=" << apiKey 
                  << "&client_secret=" << apiSecret 
                  << "&grant_type=client_credentials"; // Ensure grant_type is set

    std::string payload = payloadStream.str();

    std::string response = makeApiRequest(endpoint, payload, "POST");
    auto jsonResponse = nlohmann::json::parse(response);

    if (jsonResponse.contains("result") && jsonResponse["result"].contains("access_token")) {
        accessToken = jsonResponse["result"]["access_token"];
        refreshToken = jsonResponse["result"]["refresh_token"];
        tokenExpiry = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now()) 
                      + jsonResponse["result"]["expires_in"].get<long>();
    } else {
        std::cerr << "Authentication failed: " << jsonResponse.dump() << std::endl;
    }

    return response; // Return response for logging/debugging purposes
}

std::string APIClient::refreshAccessToken() {
    std::string endpoint = "https://test.deribit.com/api/v2/public/auth";
    std::ostringstream payloadStream;
    payloadStream << "client_id=" << apiKey 
                  << "&client_secret=" << apiSecret 
                  << "&grant_type=client_credentials"; // Ensure grant_type is set

    std::string payload = payloadStream.str();

    std::string response = makeApiRequest(endpoint, payload, "POST");
    auto jsonResponse = nlohmann::json::parse(response);

    if (jsonResponse.contains("result") && jsonResponse["result"].contains("access_token")) {
        accessToken = jsonResponse["result"]["access_token"];
        refreshToken = jsonResponse["result"]["refresh_token"];
        tokenExpiry = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now()) 
                      + jsonResponse["result"]["expires_in"].get<long>();
    } else {
        std::cerr << "Token refresh failed: " << jsonResponse.dump() << std::endl;
    }

    return response; // Return response for logging/debugging purposes
}

std::string APIClient::placeOrder(const std::string& instrumentName, double amount, const std::string& direction, const std::string& orderType, double price) {
    std::string method = (direction == "buy") ? "private/buy" : "private/sell";
    std::string endpoint = "https://test.deribit.com/api/v2/" + method;

    std::ostringstream payloadStream;
    payloadStream << "amount=" << amount 
                  << "&instrument_name=" << instrumentName 
                  << "&label=market0000234&" 
                  << "type=" << orderType;

    if (orderType == "limit") {
        payloadStream << "&price=" << price; // Include price for limit orders
    }

    std::string payload = payloadStream.str();
    
    // Output the cURL request for placing an order
    std::string curlRequest = "curl -X POST \"" + endpoint + "\" -H \"Authorization: Bearer " + accessToken + "\" -H \"Content-Type: application/x-www-form-urlencoded\" --data \"" + payload + "\"";
    std::cout << "cURL Request: " << curlRequest << std::endl;

    // Make the API request
    std::string response = makeApiRequest(endpoint, payload, "POST", accessToken);

    // Print the order response
    std::cout << "Order Response: " << response << std::endl;

    return response;
}

std::string APIClient::makeApiRequest(const std::string& endpoint, const std::string& payload, const std::string& method, const std::string& token) {
    CURL* curl = curl_easy_init();
    std::string response;

    if (curl) {
        // Set URL
        curl_easy_setopt(curl, CURLOPT_URL, endpoint.c_str());

        // Set HTTP method
        if (method == "POST") {
            curl_easy_setopt(curl, CURLOPT_POST, 1L);
            curl_easy_setopt(curl, CURLOPT_POSTFIELDS, payload.c_str());
        } else if (method == "GET") {
            curl_easy_setopt(curl, CURLOPT_HTTPGET, 1L);
        }

        // Set the Authorization header if a token is provided
        struct curl_slist* headers = nullptr;
        headers = curl_slist_append(headers, "Content-Type: application/x-www-form-urlencoded");
        if (!token.empty()) {
            std::string authHeader = "Authorization: Bearer " + token;
            headers = curl_slist_append(headers, authHeader.c_str());
        }
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        // Set write callback to capture the response
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, +[](char* ptr, size_t size, size_t nmemb, std::string* data) {
            data->append(ptr, size * nmemb);
            return size * nmemb;
        });
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);

        // Perform the request
        CURLcode res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            std::cerr << "cURL error: " << curl_easy_strerror(res) << std::endl;
        }

        // Clean up
        curl_easy_cleanup(curl);
        curl_slist_free_all(headers);  // Free the headers list
    } else {
        std::cerr << "Failed to initialize cURL." << std::endl;
    }

    return response;
}
