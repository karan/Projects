#include <iostream>
#include <fstream>
#include <sstream>

#define MAX_POINTS 100000

using namespace std;

int p[MAX_POINTS][2];
int N;

int dist(int p1[], int p2[]) {
	return ((p1[0] - p2[0]) < 0 ? p2[0] - p1[0] : p1[0] - p2[0]) + ((p1[1] - p2[1]) < 0 ? p2[1] - p1[1] : p1[1] - p2[1]);
}

int main() {

	ifstream fin;
	fin.open("marathon.in");
	fin >> N;

	int d = 0;
	for (int pt = 0; pt < N; ++pt) {
		fin >> p[pt][0] >> p[pt][1];
		if (pt > 0) {
			d += dist(p[pt-1], p[pt]);
			//cout << d << ":" << dist(p[pt-1], p[pt]) << "\n";
		}
	}

	//cout << d;

	fin.close();

	int maxskip = 0;
	for (int skip = 1; skip < N-1; ++skip) {
		int s = dist(p[skip-1], p[skip+1]) - (dist(p[skip-1], p[skip]) + dist(p[skip], p[skip+1]));
		if (s < maxskip) {
			maxskip = s;
		}
		cout << s;
	}

	ofstream fout;
	fout.open("marathon.out");
	fout << d + maxskip;
	fout.close();
	return 0;
}
