#include <iostream>
using namespace std;
class BaseClass
{
private:
    int data;

public:
    BaseClass(int d) : data(d) {}
    friend class FriendClass;
};

class FriendClass
{
public:
    FriendClass() {}
    int getBaseClassValue(BaseClass &bObj)
    {
        return bObj.data;
    }
};

int main()
{
    BaseClass bclass(5);
    FriendClass fclass;
    int res = fclass.getBaseClassValue(bclass);
    cout << res << endl;
    return 0;
}