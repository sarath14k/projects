#include <iostream>
#include <string>
#include <algorithm>
#include <openssl/hmac.h>
#include <openssl/evp.h>
#include <openssl/buffer.h>

using namespace std;

std::string hmacSha256(const std::string &data, const std::string &key);
std::string base64UrlEncode(const std::string &input);
std::string base64UrlDecode(const std::string &input);
std::string createJWT(const std::string &headerJson, const std::string &payloadJson, const std::string &secret);
bool validateJWT(const std::string &jwt, const std::string &secret);

int main()
{
    std::string headerJson = R"({"alg": "HS256", "typ": "JWT"})";
    std::string payloadJson = R"({"sub": "1234567890", "name": "John Doe", "iat": 1516239022})";
    std::string secret = "your-256-bit-secret";

    std::string jwt = createJWT(headerJson, payloadJson, secret);
    std::cout << "JWT: " << jwt << std::endl;

    bool isValid = validateJWT(jwt, secret);
    std::cout << "Is JWT valid? " << (isValid ? "Yes" : "No") << std::endl;

    return 0;
}

std::string hmacSha256(const std::string &data, const std::string &key)
{
    unsigned char *digest;
    unsigned int len = EVP_MAX_MD_SIZE;
    digest = new unsigned char[len];

    HMAC(EVP_sha256(), key.data(), key.size(),
         reinterpret_cast<const unsigned char *>(data.data()), data.size(),
         digest, &len);

    std::string hash(reinterpret_cast<char *>(digest), len);
    delete[] digest;
    return hash;
}

std::string hmacSha256(const std::string &data, const std::string &key)
{
    unsigned char digest[EVP_MAX_MD_SIZE];
    unsigned int len = 0;

    HMAC(EVP_sha256(), key.data(), key.size(),
         reinterpret_cast<const unsigned char *>(data.data()), data.size(),
         digest, &len);

    return std::string(reinterpret_cast<char *>(digest), len);
}

std::string createJWT(const std::string &headerJson, const std::string &payloadJson, const std::string &secret)
{
    std::string header = base64UrlEncode(headerJson);
    std::string payload = base64UrlEncode(payloadJson);
    std::string headerAndPayload = header + "." + payload;
    std::string signature = base64UrlEncode(hmacSha256(headerAndPayload, secret));
    return header + "." + payload + "." + signature;
}

std::string base64UrlEncode(const std::string &
