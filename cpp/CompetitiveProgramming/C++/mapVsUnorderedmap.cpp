#include <iostream>
#include <map>
#include <unordered_map>
using namespace std;

int main()
{
    map<int, string> userMap;
    userMap[3] = "Shameem";
    userMap[2] = "Shamil";
    userMap[1] = "adhil";
    userMap.insert(make_pair(0, "Anu"));

    for (auto &it : userMap)
    {
        cout << it.first << " " << it.second << endl;
    }

    // map follows Self balanced BST (Binary Search Tree) like Red Black Tree or AVL
    //  we can use if we need the output in sorted order of key only
    //  less effcient and time and space complex than unordered_map

    unordered_map<int, string> sampleMap;
    sampleMap[1] = "Hi";
    sampleMap[5] = "Hello";
    sampleMap[3] = "hey";

    unordered_map<int, string>::iterator it;
    for (it = sampleMap.begin(); it != sampleMap.end(); ++it)
    {
        cout << it->first << " " << it->second << endl;
    }

    // unordered_map follows hashing ,so more effcient to store and retieve data

    return 0;
}