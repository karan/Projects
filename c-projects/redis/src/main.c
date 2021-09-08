#include <hiredis/hiredis.h>
#include <stdio.h>
#include <stdlib.h>
#include "redis-cli.h"
#include <stdbool.h>
#include <string.h>


int main(int argc,char* argv[]) {
	
	if (argc<2) {
		fprintf(stderr,"Usage: %s <command>\n",argv[0]);
		return -1;
	}

	char* pass = getPass();

	if (!pass) {
		fprintf(stderr,"Missing REDIS_PASSWORD variable\n");
		abort();
	}

	struct Config* config = malloc(sizeof(struct Config));

	readConfig(config);			
	
	redisContext* ctx = init(config->hostname,config->port,pass); // connecting and authenticating to server
	free(config);
	
	checkConnection(ctx); // checking connection

	char* cmd = malloc(1024);	

	strcpy(cmd,argv[1]);
	strcat(cmd," ");

	for (int i=2;i<argc;i++) {
		strcat(cmd,argv[i]);
		strcat(cmd," ");
	
	}
	printf("Running: %s\n",cmd);
	runCommand(ctx,cmd);

	free(cmd);	
	
	
	return 0;
}






