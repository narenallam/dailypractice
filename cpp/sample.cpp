
#include <iostream>
using namespace std;

int main(int argc, char **argv, char **env) {
  cout << "Hello Rossum!" << endl;
  

  int x = 20;
  int *p = &x;
  int &r = x;
  int &&rr = 20;

  cout << "x: "<< x << endl;
  cout << "&x: " << &x << endl;
  cout << "p: " << p << endl;
  cout << "*p: " << *p << endl;
  cout << "r: " << r << endl;
  cout << "&r: " << &r << endl;
  cout << "rr: " << rr << endl;
  return 0;
}
