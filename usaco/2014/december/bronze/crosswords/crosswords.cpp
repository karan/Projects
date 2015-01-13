#include <iostream>
#include <fstream>
#include <sstream>

#define MAX_ROW 50
#define MAX_COL 50

using namespace std;

char grid[MAX_COL][MAX_ROW];
int numans;
int N, M;

int main() {
	
	numans = 0;
	stringstream ans;

	ifstream fin;
	fin.open("crosswords.in");

	fin >> N >> M;

	for (int row = 0; row < N; ++row) {
		for (int col = 0; col < M; ++col) {
			fin >> grid[row][col];
		}
	}
	
	fin.close();

	for (int row = 0; row < N; ++row) {
		for (int col = 0; col < M; ++col) {
			if (grid[row][col] == '.') {
				if (col < 48 && // enough space to right
				   (col == 0 || grid[row][col-1] == '#') && // space to left is beyond or #
				   (grid[row][col+1] == '.' && grid[row][col+2] == '.')) { // spaces to right are .
					ans << "\n" << row+1 << " " << col+1;
					numans++;
					continue;
				}
				if (row < 48 && // enough space below
				   (row == 0 || grid[row-1][col] == '#') && // space to top is beyond or #
				   (grid[row+1][col] == '.' && grid[row+2][col] == '.')) { // spaces to right are .
					ans << "\n" << row+1 << " " << col+1;
					numans++;
					continue;
				}
			}
		}
	}

	ofstream fout;
	fout.open("crosswords.out");
	fout << numans;
	fout << ans.rdbuf();
	fout.close();	

	return 0;
}
