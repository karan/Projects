#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <sstream>
#include <string>

using namespace std;

int main() {
	int count = 0;
	for (int i = 1; i <= 10; i++) {
		cout << "Test case " << i << ": " << "\n\n";
		
		ostringstream sin, sfin1, sfin2;
		sin << "cp .\\test_cases\\I." << i << " digits.in";
		string st = sin.str();
		system(st.c_str());
		system("digits.exe");

		ifstream fin1, fin2;
		sfin1 << "digits.out";
		sfin2 << "./test_cases/O." << i;
		fin1.open(sfin1.str().c_str());
		fin2.open(sfin2.str().c_str());

		int n1, n2;
		fin1 >> n1;
		fin2 >> n2;

		cout << "Output\tExpected\n";
		
		cout << n1 << "\t" << n2 << '\n';
		
		if (n1 == n2) {
			cout << "Correct\n\n\n";
			count++;
		}	
		else
			cout << "Incorrect\n\n\n";
	}


	if (count == 0)
		cout << "All test cases wrong.";
	else if (count < 10)
		cout << count << " test cases wrong.";
	else if (count == 10)
		cout << "All test cases correct.";


	return 0;
}
