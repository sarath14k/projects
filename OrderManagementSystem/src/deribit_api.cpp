#include "deribit_api.h"
#include <nlohmann/json.hpp>

DeribitAPI::DeribitAPI() {
    authenticate();
}

void DeribitAPI::setAccessToken(const std::string& token) {
    accessToken = token;
}

std::string DeribitAPI::performRequest(const std::string& url, const std::string& data, const std::string& method) {
    CURL* curl;
    CURLcode res;
    std::string readBuffer;

    curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        if (!data.empty()) {
            curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data.c_str());
        }
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        struct curl_slist* headers = NULL;
        headers = curl_slist_append(headers, ("Authorization: Bearer " + accessToken).c_str());
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        if (method == GET) {
            curl_easy_setopt(curl, CURLOPT_HTTPGET, 1L);
        } else {
            curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, method.c_str());
        }

        res = curl_easy_perform(curl);
        curl_easy_cleanup(curl);
        curl_slist_free_all(headers);
    }

    return readBuffer;
}

size_t DeribitAPI::WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

std::string DeribitAPI::authenticate() {
    std::string url = BASE_URL + "public/auth?client_id=" + API_KEY + "&client_secret=" + CLIENT_SECRET + "&grant_type=client_credentials";
    std::string response = performRequest(url, "", GET);

    auto jsonResponse = nlohmann::json::parse(response);
    std::string token = jsonResponse["result"]["access_token"];
    std::cout << "\nAccess Token = " << token << std::endl;
    setAccessToken(token);
    return token;
}

std::string DeribitAPI::placeOrder(double amount, const std::string& instrument_name, const std::string& order_type, double price) {
    std::string url = BASE_URL + "private/buy?amount=" + std::to_string(amount) + "&instrument_name=" + instrument_name + "&type=" + order_type + "&price=" + std::to_string(price);
    std::string response = performRequest(url, "", GET);
    return response;
}

std::string DeribitAPI::cancelOrder(const std::string& order_id) {
    std::string url = BASE_URL + "private/cancel?order_id=" + order_id;

    std::string response = performRequest(url, "", GET);
    return response;
}

std::string DeribitAPI::modifyOrder(const std::string& order_id, double amount, double price) {
    std::string url = BASE_URL + "private/edit?advanced=implv&amount=" + std::to_string(amount) +
                      "&order_id=" + order_id + "&price=" + std::to_string(price);

    std::string response = performRequest(url, "", GET);
    return response;
}

std::string DeribitAPI::getOrderBook(const std::string& instrument_name, int depth) {
    std::string url = BASE_URL + "public/get_order_book?depth=" + std::to_string(depth) + "&instrument_name=" + instrument_name;
    std::string response = performRequest(url, "", GET);
    return response;
}
std::string DeribitAPI::viewCurrentPositions() {
    std::string url = BASE_URL + "private/get_positions";
    std::string response = performRequest(url, "", GET);
    return response;
}
