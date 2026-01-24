/******************************************************************************

                              Online C++ Compiler.
               Code, Compile, Run and Debug C++ program online.
Write your code in this editor and press "Run" button to compile and execute it.

*******************************************************************************/

#include <iostream>
#include <set>
#include <vector>
using namespace std;
string removeDuplicate(string str){
    set<char> s;
    string res = "";
    
    if(str.length() == 0 || str =="\0"){
        cout << "No duplicates"<<endl;
    }
    
    for(char ch:str){
        if( s.find(ch)==s.end() ){
            res.push_back(ch);
            s.insert(ch);
        }
    }
    return res;
}

int main()
{

    cout << "enter the string" <<endl;
    string userInput;
    getline(cin,userInput);
    
    string res = removeDuplicate(userInput);
    cout << "result string " << res <<endl;
    return 0;
}
