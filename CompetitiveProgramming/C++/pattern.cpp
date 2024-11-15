/******************************************************************************

                              Online C++ Compiler.
               Code, Compile, Run and Debug C++ program online.
Write your code in this editor and press "Run" button to compile and execute it.

*******************************************************************************/

#include <iostream>
using namespace std;

void diagonal(){
    int limit = 5;
    for(int i=0;i<limit;i++){
        for(int j=0;j<limit;j++){
            if(i==j){
                cout << "*";
            }else{
                cout << " ";
            }
        }
        cout <<endl;
    }
}

void triangle(){
    int limit = 5;
    for(int i=0;i<limit;i++){
        for(int j=0;j<=i;j++){
            cout << "*";
        }
        cout <<endl;
    }
}

void triangleulta(){
    int limit = 5;
    for(int i=0;i<=limit;i++){
        for(int j=limit;j>=i;j--){
            cout << "*";
        }
        cout <<endl;
    }
}

void triangle2(){
    int limit = 5;
    for(int i=0;i<=limit;i++){
        for(int j=0;j<=limit;j++){
            if(i>j){
              cout << " ";  
            }else{
                cout << "*";
            }
            
        }
        cout <<endl;
    }
}

int main()
{
    //diagonal();
    //triangle();
    //triangleulta();
    triangle2();
    return 0;
}
