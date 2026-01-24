#include <iostream>
using namespace std;
bool powFun(int num){
    while(num % 3 == 0){
        num = num / 3;
    }
    return num == 1;
}

int main(){

    bool res = powFun(6);
    cout << (res ? "power" : "not power");
    return 0;
}