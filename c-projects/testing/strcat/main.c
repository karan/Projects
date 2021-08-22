#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char* argv[]) {

	char* data = malloc(1024*sizeof(char));
	data = strcat(data,"working");
	data = strcat(data,"now");
	printf("%s\n",data);
	return 0;
	
}
