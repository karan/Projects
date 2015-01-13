#include <iostream>
#include <fstream>
#include <sstream>

#define MAX_COWS 100000

using namespace std;

int cows[MAX_COWS];
int N;

/*
string printcows() {
	stringstream ret;
	ret << "[";
	for (int c = 0; c < N; ++c) {
		ret << cows[c];
		if (c < N-1) {
			ret << ", ";
		}
	}
	ret << "]";
	return ret.str();
}
*/

int main() {
	
	ifstream fin;
	fin.open("cowjog.in");
	fin >> N;
	int a;
	for (int c = 0; c < N; ++c) {
		fin >> a >> cows[c];
	}
	fin.close();
	//cout << printcows() << "\n";	

	int groups = 1;
	
	for (int c = N-1; c > 0; --c) {
		if (cows[c] >= cows[c-1]) {
			++groups;
		}
		else {
			cows[c-1] = cows[c];
		}
		//cout << printcows() << "\n";
	}	

	ofstream fout;
	fout.open("cowjog.out");
	fout << groups;
	//cout << groups;
	fout.close();

	return 0;
}
