#include <iostream>
#include <fstream>

#define MAX_ADJ 30
#define MAX_COW 100

using namespace std;

string adj[MAX_ADJ][MAX_COW];

int main() {

	ifstream fin;
	fin.open("nocow.in");

	string word;
	fin >> word;

	cout << word;

	return 0;
}
