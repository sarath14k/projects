#ifndef LZW_H
#define LZW_H

#include <string>
#include <vector>
#include <unordered_map>
#include <fstream>

class LZW {
public:
    void compress(const std::string& inputFile, const std::string& outputFile);
    void decompress(const std::string& inputFile, const std::string& outputFile);
};

#endif // LZW_H
