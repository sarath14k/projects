// Online C++ compiler to run C++ program online
#include <iostream>
#include <string>
#include <unordered_map>
using namespace std;

void mostOccr(string &str,char key){
  int count;
     
     for(char c : str){
         if(c == key){
             count++;
         }
        
     }
    cout << count<< endl;
}

int main() {
    string uStr;
    char c;
    cout << "enter the string" << endl;
    getline(cin,uStr);
    cout << "enter the key" << endl;
    cin >> c;
    mostOccr(uStr,c);

    return 0;
}