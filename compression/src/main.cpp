#include <iostream>
#include "Huffman.h"
#include "LZW.h"

int main() {
    int choice, operation;
    std::string inputFile, outputFile;

    std::cout << "File Compression Tool\n";
    std::cout << "1. Huffman Compression\n";
    std::cout << "2. LZW Compression\n";
    std::cout << "Choose a method (1/2): ";
    std::cin >> choice;

    std::cout << "Choose operation:\n";
    std::cout << "1. Compress\n";
    std::cout << "2. Decompress\n";
    std::cout << "Enter operation (1/2): ";
    std::cin >> operation;

    std::cout << "Enter input file path: ";
    std::cin >> inputFile;
    std::cout << "Enter output file path: ";
    std::cin >> outputFile;

    switch (choice) {
        case 1: { // Huffman
            Huffman huffman;
            if (operation == 1) {
                huffman.compress(inputFile, outputFile);
                std::cout << "Huffman compression completed.\n";
            } else if (operation == 2) {
                huffman.decompress(inputFile, outputFile);
                std::cout << "Huffman decompression completed.\n";
            } else {
                std::cout << "Invalid operation.\n";
            }
            break;
        }
        case 2: { // LZW
            LZW lzw;
            if (operation == 1) {
                lzw.compress(inputFile, outputFile);
                std::cout << "LZW compression completed.\n";
            } else if (operation == 2) {
                lzw.decompress(inputFile, outputFile);
                std::cout << "LZW decompression completed.\n";
            } else {
                std::cout << "Invalid operation.\n";
            }
            break;
        }
        default:
            std::cout << "Invalid choice.\n";
            break;
    }

    return 0;
}
