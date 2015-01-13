#include <iostream>
#include <fstream>

#define MAX 50

char map[MAX][MAX];
int N, M;

using namespace std;

void printlines() {
	for (int x = 0; x < N; x++) {
		for (int y = 0; y < M; y++) {
			cout << map[x][y];
		}
		cout << '\n';
	}
}

void fill(int x, int y, char c) {
	if (x < 0 || x >= N || y < 0 || y >= M) return;
	if (map[x][y] != 'X') return;
	if (map[x+1][y] == '.' || map[x][y+1] == '.' ||
	    map[x-1][y] == '.' || map[x][y-1] == '.')
		map[x][y] = (char)(c-'1'+'A');
	else map[x][y] = c;
	//cout << "(" << x << "," << y << ") -> " << map[x][y] << '\n';
	//printlines();
	fill(x+1, y, c);
	fill(x, y+1, c);
	fill(x-1, y, c);
	fill(x, y-1, c);
}

int abs(int a) {
	if (a < 0) return a*-1;
	return a;
}

int main() {
	ifstream fin;
	fin.open("pageant.in");

	fin >> N >> M;
	for (int x = 0; x < N; x++) {
		for (int y = 0; y < M; y++) {
			fin >> map[x][y];
		}
	}
	
	fin.close();

	int replace = 1;
	for (int x = 0; x < N; x++) {
		for (int y = 0; y < M; y++) {
			if (map[x][y] == 'X') {
				fill(x,y,(char)('0'+replace++));
			}
		}
	}
	
	int min = 1000;
	for (int x1 = 0; x1 < N; x1++)
		for (int y1 = 0; y1 < M; y1++)
			if (map[x1][y1] == 'A')
				for (int x2 = 0; x2 < N; x2++)
					for (int y2 = 0; y2 < M; y2++)
						if (map[x2][y2] == 'B')
							if (abs(x2-x1)+abs(y2-y1) < min)
								min = abs(x2-x1)+abs(y2-y1);

	ofstream fout;
	fout.open("pageant.out");
	fout << min-1;
	fout.close();

	return 0;
}
