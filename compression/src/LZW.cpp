#include "LZW.h"
#include "FileHandler.h"
#include <iostream>
#include <unordered_map>
#include <vector>
#include <bitset>
#include <fstream>

void LZW::compress(const std::string& inputFile, const std::string& outputFile) {
    // Read the input file
    std::string input = FileHandler::readFile(inputFile);
    std::unordered_map<std::string, int> dictionary;
    std::vector<int> output;

    // Initialize the dictionary with single character strings
    for (int i = 0; i < 256; ++i) {
        dictionary[std::string(1, (char)i)] = i;
    }

    std::string current = "";
    int dictSize = 256; // Starting size of the dictionary

    for (char ch : input) {
        std::string combined = current + ch;

        // If the combination is in the dictionary, continue
        if (dictionary.count(combined)) {
            current = combined;
        } else {
            // Output the code for current
            output.push_back(dictionary[current]);

            // Add combined to the dictionary
            dictionary[combined] = dictSize++;
            current = std::string(1, ch);
        }
    }

    // Output the code for the last sequence
    if (!current.empty()) {
        output.push_back(dictionary[current]);
    }

    // Write the compressed data to the output file
    std::ofstream out(outputFile, std::ios::binary);
    for (int code : output) {
        out.write((char*)&code, sizeof(code));
    }
    out.close();
}

void LZW::decompress(const std::string& inputFile, const std::string& outputFile) {
    std::ifstream in(inputFile, std::ios::binary);
    std::vector<int> inputCodes;
    int code;

    // Read the compressed data from the input file
    while (in.read((char*)&code, sizeof(code))) {
        inputCodes.push_back(code);
    }
    in.close();

    // Initialize the dictionary
    std::unordered_map<int, std::string> dictionary;
    for (int i = 0; i < 256; ++i) {
        dictionary[i] = std::string(1, (char)i);
    }

    std::string current = "";
    std::string result = "";
    int dictSize = 256; // Starting size of the dictionary

    for (size_t i = 0; i < inputCodes.size(); ++i) {
        int currentCode = inputCodes[i];

        // If the current code is in the dictionary
        if (dictionary.count(currentCode)) {
            result += dictionary[currentCode];

            // Create new entry in the dictionary
            if (!current.empty()) {
                dictionary[dictSize++] = current + dictionary[currentCode][0];
            }

            current = dictionary[currentCode];
        } else {
            // Handle the case where the code is not in the dictionary
            if (current.empty()) {
                result += dictionary[currentCode];
            } else {
                std::string entry = current + current[0];
                result += entry;
                dictionary[dictSize++] = entry;
            }
        }
    }

    // Write the decompressed data to the output file
    FileHandler::writeFile(outputFile, result);
}
