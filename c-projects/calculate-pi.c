#include <stdio.h>
#include <math.h>


int main() {
	long PI = 4 * atan(1/5) - atan(1/239);
	PI = PI * 4;	
	printf("%lD\n",PI); 
	return 0;
}
