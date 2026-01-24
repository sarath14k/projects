#ifndef HUFFMAN_H
#define HUFFMAN_H

#include <string>
#include <unordered_map>
#include <queue>
#include <vector>
#include <fstream>
#include <bitset>

// Definition of HuffmanNode
struct HuffmanNode {
    char character;
    int frequency;
    HuffmanNode* left;
    HuffmanNode* right;

    HuffmanNode(char ch, int freq) : character(ch), frequency(freq), left(nullptr), right(nullptr) {}
};

// Comparator for the priority queue
struct Compare {
    bool operator()(HuffmanNode* left, HuffmanNode* right) {
        return left->frequency > right->frequency; // Min-heap based on frequency
    }
};

class Huffman {
public:
    Huffman();

    void compress(const std::string& inputFile, const std::string& outputFile);
    void decompress(const std::string& inputFile, const std::string& outputFile);

private:
    std::priority_queue<HuffmanNode*, std::vector<HuffmanNode*>, Compare> minHeap;
    std::unordered_map<char, std::string> huffmanCodes;
    std::string encodedString;
    std::string decodedString;

    void buildHuffmanTree(const std::string& input);
    void generateCodes(HuffmanNode* root, const std::string& code);
    void destroyTree(HuffmanNode* node);
    void writeCompressedFile(const std::string& outputFile);
    void readCompressedFile(const std::string& inputFile);
    void decode(const std::string& encoded);
    void writeDecompressedFile(const std::string& outputFile);
};

#endif // HUFFMAN_H
