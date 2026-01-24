#include <iostream>
#include <string>
using namespace std;

void splitInput(const std::string &input)
{
    size_t pos = 0;
    size_t len = input.size();

    string sTotalLen = input.substr(pos, 3);
    int TotalLen = stoi(sTotalLen);

    pos = pos + 3;

    while (pos < len)
    {

        // 0330107shameem0208mohammed0306kerala

        string id = input.substr(pos, 2);

        pos = pos + 2;

        string sItemLength = input.substr(pos, 2);
        int itemLength = stoi(sItemLength);

        pos = pos + 2;

        string item = input.substr(pos, itemLength);

        pos = pos + itemLength;

        cout << id << " " << item << endl;
    }
}

int main()
{
    std::string input = "0330107shameem0208mohammed0306kerala";
    splitInput(input);
    return 0;
}
