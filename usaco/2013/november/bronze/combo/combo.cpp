#include <iostream>
#include <fstream>

#define DIALS 3

using namespace std;

int N;
int farmer[DIALS], master[DIALS];

int abs(int num) {
	return num < 0 ? -num : num;
}

bool close(int a, int b) {
	int K = abs(a - b);
	return (K <= 2 || N - K <= 2);	
}

int main() {
	int count = 0;

	ifstream fin;
	fin.open("combo.in");

	fin >> N;
	for (int i = 0; i < 3; i++)
		fin >> farmer[i];
	for (int i = 0; i < 3; i++)
		fin >> master[i];
	fin.close();

	close(1, 49);

	for (int first = 1; first <= N; first++) {
		for (int second = 1; second <= N; second++) {
			for (int third = 1; third <= N; third++) {
				if (close(first, farmer[0]) && close(second, farmer[1]) && close(third, farmer[2])) {
					count++;	
				//	cout << first << " " << second << " " << third << "\n";
					continue;
				}
				if (close(first, master[0]) && close(second, master[1]) && close(third, master[2])) {
					count++;
				//	cout << first << " " << second << " " << third << "\n";
					continue;
				}
			}
		}
	}

	ofstream fout;
	fout.open("combo.out");
	fout << count;
	fout.close();
}
