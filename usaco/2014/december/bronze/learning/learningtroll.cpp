#include <fstream>

using namespace std;

int main() {
	ofstream fout;
	fout.open("learning.out");
	fout << "6";
	fout.close();
}
