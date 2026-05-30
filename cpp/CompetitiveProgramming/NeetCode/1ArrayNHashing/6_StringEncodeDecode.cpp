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

    /*
     * =======================================================
     * DEBUGGER TRACE (Visualizing Encode / Decode)
     * =======================================================
     * Encode (input = {"hello", "world", "test"}):
     *   - str = "hello" -> enc_string += "hello|"
     *   - str = "world" -> enc_string += "world|"
     *   - str = "test"  -> enc_string += "test|"
     *   - Final encoded: "hello|world|test|"
     * 
     * Decode (enc_string = "hello|world|test|"):
     *   - Char Loop: 'h', 'e', 'l', 'l', 'o' -> temp = "hello"
     *   - Hit '|' -> strList.emplace_back("hello"), temp.clear()
     *   - Char Loop: 'w', 'o', 'r', 'l', 'd' -> temp = "world"
     *   - Hit '|' -> strList.emplace_back("world"), temp.clear()
     *   - Char Loop: 't', 'e', 's', 't' -> temp = "test"
     *   - Hit '|' -> strList.emplace_back("test"), temp.clear()
     *   - Return strList: ["hello", "world", "test"]
     * 
     * Time Complexity: O(N) - Where N is the total number of characters across all strings.
     * Space Complexity: O(N) - We need extra space to build the encoded string and decode it back into a list.
     * =======================================================
     */

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
