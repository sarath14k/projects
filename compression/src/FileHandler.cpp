#include "FileHandler.h"
#include <fstream>

std::string FileHandler::readFile(const std::string& filename) {
    std::ifstream file(filename);
    std::string content((std::istreambuf_iterator<char>(file)),
                         (std::istreambuf_iterator<char>()));
    return content;
}

void FileHandler::writeFile(const std::string& filename, const std::string& content) {
    std::ofstream file(filename);
    file << content;
}
