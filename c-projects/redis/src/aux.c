#include "redis-cli.h"
#include <string.h>
#include <stdlib.h>
#include <jansson.h>


redisContext* init(char* hostname,int port,char* pass) {
	redisContext* ctx = redisConnect(hostname,port);
	if(authenticate(ctx,pass)) {
		return ctx;
	}
	else {
		return NULL;
	}
	
}

bool errorCheck(redisReply* r) {
	 return (r->type == REDIS_REPLY_ERROR) ? true:false;
 }

void cleaning(redisReply* response) {
	freeReplyObject(response);
}

bool authenticate(redisContext* ctx,char* pass) {
	if(!ctx) {
		return false;
	}
	redisReply* response = redisCommand(ctx,"AUTH %s",pass);

	if(errorCheck(response)) {
		perror(response->str);
		cleaning(response);
		return false;
	}
	else {
			cleaning(response);
			return true;
		}
		
	}

void runCommand(redisContext* ctx,char* command) {
    redisReply* response = redisCommand(ctx,command);
	
    switch (response->type) {
    case REDIS_REPLY_INTEGER:
        printf("Received reply: %lld\n",response->integer);
        break;
    case REDIS_REPLY_NIL:
         printf("Received no reply\n");
         break;
    case REDIS_REPLY_VERB:
    case REDIS_REPLY_STATUS:
    case REDIS_REPLY_STRING:
        printf("Received reply: %s\n",response->str);
        break;
    case REDIS_REPLY_DOUBLE:
        printf("Received reply: %f\n",response->dval);
        break;
    case REDIS_REPLY_ERROR:
        printf("Error: %s\n",response->str);
        break;

        
}

	cleaning(response);
}

void checkConnection(redisContext* ctx) {
    if(!ctx || ctx->err) {
		if (!ctx) {
			abort();
		}
		fprintf(stderr,"[*]Error connecting to Redis server: %s",ctx->errstr);
		abort();
	}
	printf("[*]Connected and authenticated to Redis server\n");
	printf("\n");
}
char* getPass() {
	return getenv("REDIS_PASSWORD");
}

void readConfig(struct Config* conf) {
	FILE* configFile = fopen("./conf.json","r");
	if (!configFile) {
		perror("Error");

	}
	json_error_t* err;
	json_t* config = json_object();
	config = json_loadf(configFile,JSON_DECODE_ANY,err);
	if(err) {
		fprintf(stderr,"%s",err->text);
	}

	json_t* host = json_string(NULL);
	json_t* port = json_integer(0);

	host = json_object_get(config,"hostname");
	port = json_object_get(config,"port");
	
	char* hostname = malloc(512);
	sprintf(hostname,"%s",json_string_value(host));
	
	conf->hostname = hostname;
	conf->port = json_integer_value(port);
	free(hostname);
	
	
	json_decref(config);
	json_decref(host);
	json_decref(port);

	fclose(configFile);

}
