#include <iostream>
#include <string>
using namespace std;

int main()
{
   char name[3] = {'c', 'e', 'f'};
   string str = "";
   for (char c : name)
   {
      str.push_back(c);
   }

   cout << str << endl;
   cout << str.length() << endl;

   char ch[3] = {'a', 'b', 'c'};
   string chStr(ch, sizeof(ch));
   cout << chStr << endl;
   cout << chStr.length() << endl;
   return 0;
}
