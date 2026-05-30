#include <iostream>
using namespace std;

#include "ToyFactory.cpp"

int main() {

  int type;
  while (true) {
    cout << endl << "Enter type or Zero for exit" << endl;
    cin >> type;

    if (!type)
      break;

    Toy *v = ToyFactory::createToy(type);

    if (v) {
      v->showProduct();
      delete v;
    }
  }
  cout << "Exit.." << endl;

  return 0;
}
