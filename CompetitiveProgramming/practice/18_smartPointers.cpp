#include <iostream>
#include <memory>
using namespace std;

class Resource{
    private:
        string _name;
    public:
        Resource(const string& name) : _name(name){
            cout << _name << " created!\n";
        }
        ~Resource() {
            cout << _name << " destroyed!\n";
        }
        void show() {
            cout << "Using resource : " << _name << endl;
        }
};

int main()
{
    unique_ptr<Resource> res1 = make_unique<Resource>("Unique Resource");
    res1->show();
    shared_ptr<Resource> res2 = make_shared<Resource>("Shared Resource");
    res2->show();
    shared_ptr<Resource> res3 = res2;
    cout << "Shared count: " << res2.use_count() << endl;
    weak_ptr<Resource> weakRes = res2;
    cout << "Shared count after weak_ptr : " << res2.use_count() << endl;
    if(auto sharedFromWeak = weakRes.lock())
        sharedFromWeak->show();
    else
        cout << "Resource no longer exists\n";
}
