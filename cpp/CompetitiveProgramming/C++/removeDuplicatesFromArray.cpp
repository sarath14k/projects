#include <iostream>
#include <string>
#include <set>
#include <vector>
using namespace std;

vector<int> removeDuplicate(int arr[],int size) {
    set<int> s;
    vector<int> res;
    if(size == 1){
        cout << "No Duplicates" << endl;
        
    }else{
        for(int i = 0;i<size;i++){
            if (s.find(arr[i]) == s.end()) {
                res.push_back(arr[i]);
                s.insert(arr[i]);
            }
        }
    }
    
   return res;
}

int main() {
    int arr[] = {1,4,1,2,3};
    //int arr[] = {1};
    int size = sizeof(arr)/sizeof(arr[0]);
    vector<int>result = removeDuplicate(arr,size);
    if(result.size()){
        cout <<"after removing duplicates" << endl;
        for(int element : result){
            cout << element << " ";
        }
    }
    
    return 0;
}
