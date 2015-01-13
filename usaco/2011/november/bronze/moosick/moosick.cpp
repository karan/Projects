#include <iostream>
#include <fstream>
#include <algorithm>

#define MAX_N 20000
#define MAX_C 10

int notes[MAX_N];
int chord[MAX_C];
int temp_chord[MAX_C];
int bad_notes[MAX_N];
int bad_notes_p = 0;
int N, C;

using namespace std;

void print(int a[]) {
	cout << "[";
	for (int i = 0; i < sizeof(a) - 1; i++) {
		cout << a[i];
		if (i < sizeof(a) - 2)
			cout << ",";
	}
	cout << "]\n";

}

int main() {
	ifstream fin;
	fin.open("moosick.in");

	fin >> N;
	for (int i = 0; i < N; i++)
		fin >> notes[i];
	fin >> C;
	for (int i = 0; i < C; i++)
		fin >> chord[i];
	
	fin.close();
	
	sort(chord, chord + C);
	//print(chord);
	for (int i = 1; i < C; i++)
		chord[i] -= chord[0];
	chord[0] = 0;

	int count = 0;
	for (int i = 0; i + C - 1 < N; i++) {
		for (int j = i; j < i + C; j++)
		       	temp_chord[j-i] = notes[j];
		sort(temp_chord, temp_chord + C);
		//print(temp_chord);
		for (int j = 1; j < C; j++)
			temp_chord[j] -= temp_chord[0];
		temp_chord[0] = 0;
		bool all_true = true;
		for (int j = 0; j < C; j++)
			if (chord[j] != temp_chord[j])
				all_true = false;
		if (all_true) {
			count++;
			bad_notes[bad_notes_p++] = i;
		}
	}
	
	ofstream fout;
	fout.open("moosick.out");

	fout << count;
	
	for (int i = 0; i < count; i++)
		fout << '\n' << bad_notes[i] + 1;

	fout.close();
	
	return 0;
}
