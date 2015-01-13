#include <iostream>
#include <fstream>
#include <algorithm>
#include <sstream>

#define MAX_COWS 50000

using namespace std;

struct cow {
	bool spotted;
	int weight;
};

cow cows[MAX_COWS];
int N, A, B;

string printcows() {
	stringstream ret;
	ret << "[";
	for (int i = 0; i < N; ++i) {
		ret << "[" << (cows[i].spotted ? "S," : "NS,") << cows[i].weight << "]";
		if (i < N-1) {
			ret << ", ";
		}
	}
	ret << "]";
	return ret.str();
}

bool alg(cow a, cow b) {
	return a.weight < b.weight;
}

int main() {
	
	ifstream fin;
	fin.open("learning.in");
	fin >> N >> A >> B;
	
	string pl = "";
	for (int c=0; c < N; ++c) {
		fin >> pl >> cows[c].weight;
		cows[c].spotted = (pl == "S");
	}
	
	fin.close();

	sort(cows, cows+N, alg);

	if (N < MAX_COWS) {
		cow tcow;
		tcow.spotted = 0;
		tcow.weight = cows[N-1].weight + 1;
		cows[N+1] = tcow;
	}

	int s, e;
	
	cout << printcows() << "\n";
	
	int total = 0;

	for (int c = 0; c < N; c++) {
	
	}

	ofstream fout;
	fout.open("learning.out");
	fout << total;
	cout << total;
	fout.close();

	return 0;
}
