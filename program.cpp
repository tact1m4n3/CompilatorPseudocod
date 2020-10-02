#include <iostream>
using namespace std;

int main() {
    int a;
    float b;
    float c;
    cin >> a >> b;
    if((a>b)){
        c=(a-b);
    }
    else{
        c=(b-a);
    }
    cout << c;
}