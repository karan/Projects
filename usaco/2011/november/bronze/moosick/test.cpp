#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <sstream>
#include <string>

using namespace std;

int main() {
	for (int i = 1; i <= 10; i++) {
		ostringstream sin, sfin1, sfin2;
		sin << "cp .\\test_cases\\I." << i << " moosick.in";
		string st = sin.str();
		system(st.c_str());
		cout << st << '\n';
		system("moosick.exe");

		ifstream fin1, fin2;
		sfin1 << "moosick.out";
		sfin2 << "./test_cases/O." << i;
		fin1.open(sfin1.str().c_str());
		fin2.open(sfin2.str().c_str());

		int n1, n2;
		fin1 >> n1;
		fin2 >> n2;

		cout << "Test case " << i << ": " << "\n";
		//cout << "Output\tExpected\n";

		int a, b;
		bool right = true;
		if (n1 != n2)
			right = false;
		cout << n1 << '\t' << n2 << '\n';
		while (n1 > 0 || n2 > 0) {
			if (n1 > 0) {
				--n1;
				fin1 >> a;
				//cout << a;
			}
			//cout << '\t';
			if (n2 > 0) {
				--n2;
				fin2 >> b;
				//cout << b;
			}
			//cout << '\n';
			if (a != b) {
				right = false;
			}
		}
		if (right)
			cout << "Correct\n";
		else
			cout << "Incorrect\n";
	}
	return 0;
}
