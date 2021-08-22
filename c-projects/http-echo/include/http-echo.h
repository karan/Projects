#include <assert.h>
#include <jansson.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <microhttpd.h>
#include <stdio.h>

#define KBLU  "\x1B[34m"
#define KNRM  "\x1B[0m" 
#define KRED  "\x1B[31m"
#define RST printf("%s\n",KNRM)
#define MSG "NOT IMPLEMENTED"

/*
Function used to get request headers
Executed FOR EACH header in place, so need to pay attention on how to collect data
*/
int getHeader(void *cls, enum MHD_ValueKind kind, const char *key, const char *value);
/* 
Request handler;
Gets executed for every call received
Collects the request headers in a JSON objects and send that back as a response
*/
int handler(void *cls, struct MHD_Connection *connection,const char *url,const char *method, const char *version,const char *upload_data,size_t *upload_data_size, void **con_cls);

/*
Function used to retrieve client IP address; took me a while to find how to do that, docs suck
*/
char* getIP(struct MHD_Connection *connection);