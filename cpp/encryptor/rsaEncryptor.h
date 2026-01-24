#ifndef RSAENCRYPTOR_H
#define RSAENCRYPTOR_H

#include <string>
#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/err.h>
#include <iostream>
#include <fstream>
#include <sstream>


class RSAEncryptor {
public:
    RSAEncryptor();
    ~RSAEncryptor();
    
    RSA *loadKey(const std::string &keyFile, bool isPublic);
    bool generateKeys(const std::string &publicKeyFile, const std::string &privateKeyFile);
    std::string encrypt(const std::string &plainText, const std::string &publicKeyFile);
    std::string decrypt(const std::string &cipherText, const std::string &privateKeyFile);
    // Public method to load keys
    bool loadPublicKey(const std::string &keyFile) {
        return loadKey(keyFile, true);
    }

    bool loadPrivateKey(const std::string &keyFile) {
        return loadKey(keyFile, false);
    }

private:
    RSA *privateRSA; // Private key
    RSA *publicRSA;  // Public key

    // Helper function to load RSA keys from files
};

#endif // RSAENCRYPTOR_H
