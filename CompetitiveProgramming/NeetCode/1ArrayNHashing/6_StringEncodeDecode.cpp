    // Decode the string back into a list of strings
    #include <iostream>
    #include <vector>
    using namespace std;

    // Function to encode a list of strings into a single string
    string encode(const vector<string>& strList) {
        string enc_string;
        for (const string& str : strList) {
            enc_string += str + "|"; // Use a delimiter for encoding
        }
        return enc_string; // Return by value, not by reference
    }

    // Function to decode a single string back into a list of strings
    vector<string> decode(const string& enc_string) {
        vector<string> strList;
        string temp;
        for (char ch : enc_string) {
            if (ch == '|') {
                strList.emplace_back(temp);
                temp.clear();
            } else
                temp += ch;

        }
        return strList;
    }

    int main() {
        vector<string> input = {"hello", "world", "test"};

        // Encode the list of strings
        string encoded = encode(input);
        cout << "Encoded String: " << encoded << endl;
        // Decode the string back into a list of strings
        vector<string> decoded = decode(encoded);
        cout << "Decoded Strings: ";
        for (const auto& str : decoded)
            cout << str << " ";
        cout << endl;
        return 0;
    }
