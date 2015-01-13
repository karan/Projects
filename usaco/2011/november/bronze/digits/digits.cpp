#include <iostream>
//#include <string> on Linux with C++11 support
#include <fstream>
#include <stdlib.h> //Windows Mingw G++ 4.8.1 does not support stoi
#include <math.h>

using namespace std;

//int base2, base3;	see line 2
string sbase2, sbase3;
long base2, base3;

int exp_tree(long num) {

	if (num == 0) return -1;
	int count;
	for (count = 0; num % 3 == 0; count++) num /= 3;
	if (num == 1) return count;
	return -1;
}

long solve() {

	long diff = base2 - base3;
//	cout << "tdiff\t\tplace\tmod\tsbase3\t+mod\t0\t2\n";
	for (int i = 0; i < sbase2.length(); i++) {
		long tdiff = diff + (-2 * (sbase2.at(sbase2.length() - 1 - i) - '0') + 1) * (long)(pow(2, i));
//		cout << tdiff << "\t";
		int modifier = 1;
		if (tdiff < 0) {
			tdiff *= -1;
			modifier *= -1;
		}
		if (tdiff % 2 == 0) {
			tdiff /= 2;
			modifier *= 2;
		}
		int place = exp_tree(tdiff);
//		if (place != -1)
//			cout << place << "\t" << modifier << "\t" << sbase3.at(sbase3.length() - 1 - place) << "\t" 
//								  << sbase3.at(sbase3.length() - 1 - place) + modifier << "\t"
//								  << '0' + 0 << "\t" << '2' + 0 << "\n";
//		else
//			cout << place << "\t" << modifier << "\t\t\t" << '0' + 0 << "\t" << '2' + 0 << "\n";
		if (place != -1 && sbase3.at(sbase3.length() - 1 - place) + modifier >= '0'
				&& sbase3.at(sbase3.length() - 1 - place) + modifier <= '2' ) {
			return base3 + modifier * pow(3, place);		
		}
	}
	return -1;

}

int main() {

	ifstream fin;
	fin.open("digits.in");
	fin >> sbase2 >> sbase3;
	
	//base2 = stoi(sbase2.c_str(), nullptr, 2);	Linux with C++11 support
	//base3 = stoi(sbase3.c_str(), nullptr, 3);	Mingw currently (as of 7/8/2014) does not support this

	base2 = strtol(sbase2.c_str(), nullptr, 2); //	On Windows Mingw G++ 4.8.1
	base3 = strtol(sbase3.c_str(), nullptr, 3);

	fin.close();
	
	ofstream fout;
	fout.open("digits.out");

	long a = solve();
	fout << a;
//	cout << a;

	fout.close();

	return 0;

/*	long a;
	cin >> a;
	while (a != -1) {
		cout << exp_tree(a) << "\n";
		cin >> a;
	}

	return 0;				*/
}
