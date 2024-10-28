#include <iostream>
#include <vector>
#include <string>

class TrieNode {
public:
    TrieNode* children[26]; // Assuming only lowercase a-z
    bool isEndOfWord;

    TrieNode() {
        isEndOfWord = false;
        for (int i = 0; i < 26; ++i) {
            children[i] = nullptr; // Initialize all children as nullptr
        }
    }
};
class Trie {
private:
    TrieNode* root;

public:
    Trie() {
        root = new TrieNode(); // Create the root node
    }

    // Insert a word into the Trie
    void insert(const std::string& word) {
        TrieNode* node = root;
        for (char c : word) {
            int index = c - 'a'; // Calculate index (assuming lowercase letters)
            if (node->children[index] == nullptr) {
                node->children[index] = new TrieNode(); // Create a new node if it doesn't exist
            }
            node = node->children[index]; // Move to the next node
        }
        node->isEndOfWord = true; // Mark the end of the word
    }

    // Search for a word in the Trie
    bool search(const std::string& word) {
        TrieNode* node = root;
        for (char c : word) {
            int index = c - 'a';
            if (node->children[index] == nullptr) {
                return false; // Not found
            }
            node = node->children[index];
        }
        return node->isEndOfWord; // Return true if it's a complete word
    }

    // Check if any word in the Trie starts with the given prefix
    bool startsWith(const std::string& prefix) {
        TrieNode* node = root;
        for (char c : prefix) {
            int index = c - 'a';
            if (node->children[index] == nullptr) {
                return false; // Prefix not found
            }
            node = node->children[index];
        }
        return true; // Prefix found
    }

    // Destructor to free memory
    ~Trie() {
        deleteTrie(root);
    }

private:
    // Helper function to delete Trie nodes
    void deleteTrie(TrieNode* node) {
        if (!node) return;
        for (int i = 0; i < 26; ++i) {
            deleteTrie(node->children[i]); // Recursively delete children
        }
        delete node; // Delete the current node
    }
};
int main() {
    Trie trie;

    // Insert words
    trie.insert("apple");
    trie.insert("app");

    // Search for words
    std::cout << std::boolalpha; // Print bool values as true/false
    std::cout << "Search 'apple': " << trie.search("apple") << std::endl; // true
    std::cout << "Search 'app': " << trie.search("app") << std::endl; // true
    std::cout << "Search 'appl': " << trie.search("appl") << std::endl; // false
    std::cout << "Starts with 'app': " << trie.startsWith("app") << std::endl; // true
    std::cout << "Starts with 'apl': " << trie.startsWith("apl") << std::endl; // false

    return 0;
}
