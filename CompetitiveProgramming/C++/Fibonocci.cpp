#include <iostream>
using namespace std;
void fibonocciSeries(int );
int main(){

    int n;
    cout << "enter the limit \t";
    cin >> n;
    fibonocciSeries(n);
    return 0;
}
void fibonocciSeries(int limit){
    //1,1,2,3,5,8,13....

    int a = 0;
    int b = 1;
    int c;
    cout << b << "\t";

    for(int i = 0; i < limit; i++){

        c = a+b;
        cout << c << "\t";
        a = b;
        b = c;
    }
}