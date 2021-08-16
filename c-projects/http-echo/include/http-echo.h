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

int getHeader(void *cls, enum MHD_ValueKind kind, const char *key, const char *value);
int handler(void *cls, struct MHD_Connection *connection,const char *url,const char *method, const char *version,const char *upload_data,size_t *upload_data_size, void **con_cls);
char* getIP(struct MHD_Connection *connection);