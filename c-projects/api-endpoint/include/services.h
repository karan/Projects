
#include <bson/bson.h>
#include <mongoc/mongoc.h>
#include <microhttpd.h>

#define KBLU  "\x1B[34m"
#define KNRM  "\x1B[0m" 
#define KRED  "\x1B[31m"
#define RST printf("%s\n",KNRM)
#define MSG "NOT IMPLEMENTED"

mongoc_collection_t* init();
char* getData( mongoc_collection_t*); 
int handler(void *cls, struct MHD_Connection *connection,const char *url,const char *method, const char *version,const char *upload_data,size_t *upload_data_size, void **con_cls);
