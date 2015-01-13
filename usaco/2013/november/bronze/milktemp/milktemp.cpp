#include <iostream>
#include <fstream>
#include <map>

using namespace std;

map<int, int> cows[2];
int N, X, Y, Z;
int maxmilk;

int main() {
	ifstream fin;
	fin.open("milktemp.in");

	fin >> N >> X >> Y >> Z;
	for (int i = 0; i < N; i++) {
		int low, high;
		fin >> low >> high;
		cows[0][low]++;
		cows[1][high]++;
	}
	
	map<int, int>::iterator low, high;
	low = cows[0].begin();
	high = cows[1].begin();
	
	maxmilk = 0;
	int milk = X * N;
	while (low != cows[0].end() && high != cows[1].end()) {
		bool lowinc = false, highinc = false;
		if (milk > maxmilk)
			maxmilk = milk;
		if (low->first <= high->first) {
			milk += (Y - X) * low->second;
			lowinc = true;	
		}
		//cout << (Y - X) * low->second << ":";
		if (low->first > high->first) {
			milk -= (Y - Z) * high->second;
			highinc = true;
		}
		//cout << (Y - Z) * high->second << " ";
		//cout << low->first << ":" << low->second << ";" << high->first << ":" << high->second << ';' << milk << '\n';
		if (lowinc) {
			++low;
		}
		if (highinc) {
			++high;
		}
	}
	
	ofstream fout;
	
	fout.open("milktemp.out");
	fout << maxmilk;
	fout.close();
}
