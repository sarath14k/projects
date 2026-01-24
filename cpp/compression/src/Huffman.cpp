#include "Huffman.h"
#include "FileHandler.h"
#include <iostream>

Huffman::Huffman() {
    // No need to initialize minHeap explicitly here; it's done automatically
}

void Huffman::compress(const std::string& inputFile, const std::string& outputFile) {
    std::string input = FileHandler::readFile(inputFile);
    buildHuffmanTree(input);
    writeCompressedFile(outputFile);
}

void Huffman::decompress(const std::string& inputFile, const std::string& outputFile) {
    readCompressedFile(inputFile);
    writeDecompressedFile(outputFile);
}

void Huffman::buildHuffmanTree(const std::string& input) {
    std::unordered_map<char, int> frequency;
    for (char ch : input) {
        frequency[ch]++;
    }

    for (const auto& pair : frequency) {
        minHeap.push(new HuffmanNode(pair.first, pair.second));
    }

    while (minHeap.size() > 1) {
        HuffmanNode* left = minHeap.top(); minHeap.pop();
        HuffmanNode* right = minHeap.top(); minHeap.pop();
        HuffmanNode* newNode = new HuffmanNode('\0', left->frequency + right->frequency);
        newNode->left = left;
        newNode->right = right;
        minHeap.push(newNode);
    }

    generateCodes(minHeap.top(), "");
}

void Huffman::generateCodes(HuffmanNode* root, const std::string& code) {
    if (!root) return;
    if (root->character != '\0') {
        huffmanCodes[root->character] = code;
    }
    generateCodes(root->left, code + "0");
    generateCodes(root->right, code + "1");
}

void Huffman::destroyTree(HuffmanNode* node) {
    if (node) {
        destroyTree(node->left);
        destroyTree(node->right);
        delete node;
    }
}

void Huffman::writeCompressedFile(const std::string& outputFile) {
    std::ofstream out(outputFile, std::ios::binary);
    if (!out) {
        std::cerr << "Error opening output file!" << std::endl;
        return;
    }

    // Write the size of the Huffman codes map
    size_t size = huffmanCodes.size();
    out.write(reinterpret_cast<const char*>(&size), sizeof(size));

    // Write each character and its code length
    for (const auto& pair : huffmanCodes) {
        char ch = pair.first;
        std::string code = pair.second;
        size_t codeLength = code.length();
        
        out.write(reinterpret_cast<const char*>(&ch), sizeof(ch));
        out.write(reinterpret_cast<const char*>(&codeLength), sizeof(codeLength));
        out.write(code.c_str(), codeLength);
    }

    // Write the encoded string
    for (char ch : encodedString) {
        out << huffmanCodes[ch];
    }

    out.close();
}

void Huffman::readCompressedFile(const std::string& inputFile) {
    std::ifstream in(inputFile, std::ios::binary);
    if (!in) {
        std::cerr << "Error opening input file!" << std::endl;
        return;
    }

    // Read the size of the Huffman codes map
    size_t size;
    in.read(reinterpret_cast<char*>(&size), sizeof(size));

    // Read each character and its code
    for (size_t i = 0; i < size; i++) {
        char ch;
        size_t codeLength;
        in.read(reinterpret_cast<char*>(&ch), sizeof(ch));
        in.read(reinterpret_cast<char*>(&codeLength), sizeof(codeLength));
        
        std::string code;
        code.resize(codeLength);
        in.read(&code[0], codeLength);
        huffmanCodes[ch] = code;
    }

    // Read the encoded string
    std::string encoded;
    char byte;
    while (in.get(byte)) {
        std::bitset<8> bits(byte);
        encoded += bits.to_string();
    }

    // Decode the encoded string using Huffman tree
    decode(encoded);
    
    in.close();
}

void Huffman::decode(const std::string& encoded) {
    HuffmanNode* currentNode = minHeap.top(); // Start from the root
    for (char bit : encoded) {
        if (bit == '0') {
            currentNode = currentNode->left;
        } else {
            currentNode = currentNode->right;
        }

        if (currentNode->character != '\0') {
            decodedString += currentNode->character; // Found a leaf
            currentNode = minHeap.top(); // Reset to root
        }
    }
}

void Huffman::writeDecompressedFile(const std::string& outputFile) {
    std::ofstream out(outputFile);
    if (!out) {
        std::cerr << "Error opening output file!" << std::endl;
        return;
    }

    out << decodedString; // Write the decoded string to output file
    out.close();
}
