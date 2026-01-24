#include "rsaEncryptor.h"
#include <iomanip>   // For std::setw and std::setfill
#include <sstream>   // For std::ostringstream

RSAEncryptor::RSAEncryptor() : privateRSA(nullptr), publicRSA(nullptr) {}

RSAEncryptor::~RSAEncryptor() {
    if (privateRSA) {
        RSA_free(privateRSA);
    }
    if (publicRSA) {
        RSA_free(publicRSA);
    }
}

bool RSAEncryptor::generateKeys(const std::string &publicKeyFile, const std::string &privateKeyFile) {
    BIGNUM *bne = BN_new();
    BN_set_word(bne, RSA_F4);
    RSA *rsa = RSA_new();
    if (!RSA_generate_key_ex(rsa, 2048, bne, nullptr)) {
        std::cerr << "Error generating RSA key." << std::endl;
        return false;
    }

    // Save the public key
    BIO *pubBio = BIO_new_file(publicKeyFile.c_str(), "w+");
    if (pubBio == nullptr || !PEM_write_bio_RSAPublicKey(pubBio, rsa)) {
        std::cerr << "Error saving public key." << std::endl;
        return false;
    }
    BIO_free_all(pubBio);

    // Save the private key
    BIO *privBio = BIO_new_file(privateKeyFile.c_str(), "w+");
    if (privBio == nullptr || !PEM_write_bio_RSAPrivateKey(privBio, rsa, nullptr, nullptr, 0, nullptr, nullptr)) {
        std::cerr << "Error saving private key." << std::endl;
        return false;
    }
    BIO_free_all(privBio);

    // Clean up
    BN_free(bne);
    RSA_free(rsa);
    return true;
}

std::string RSAEncryptor::encrypt(const std::string &plainText, const std::string &publicKeyFile) {
    publicRSA = loadKey(publicKeyFile, true);
    if (!publicRSA) {
        return "";
    }

    std::string cipherText;
    int rsaLen = RSA_size(publicRSA);
    unsigned char *encrypted = new unsigned char[rsaLen];

    int result = RSA_public_encrypt(plainText.length(), (unsigned char *)plainText.c_str(),
                                     encrypted, publicRSA, RSA_PKCS1_PADDING);
    if (result == -1) {
        std::cerr << "Error encrypting data." << std::endl;
        delete[] encrypted;
        return "";
    }

    // Convert encrypted data to hex string for easier transport
    std::ostringstream oss;
    for (int i = 0; i < result; ++i) {
        oss << std::hex << std::setw(2) << std::setfill('0') << (int)encrypted[i];
    }
    cipherText = oss.str();

    delete[] encrypted;
    return cipherText;
}
