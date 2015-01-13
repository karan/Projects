#include <iostream>
#include <fstream>

using namespace std;

int main() {

	int tminutes = -671;
	int days, hours, minutes;
	ifstream fin;
	fin.open("ctiming.in");
	
	fin >> days >> hours >> minutes;
	tminutes += 24 * 60 * (days - 11) + 60 * hours + minutes;
	if (tminutes < 0) tminutes = -1;

	ofstream fout;
	fout.open("ctiming.out");
	fout << tminutes;
}
