#include <microhttpd.h>
#include <jansson.h>
#include "services.h"

int handler(void *cls, struct MHD_Connection *connection,const char *url,const char *method, const char *version,const char *upload_data,size_t *upload_data_size, void **con_cls) {
    json_t* headers = json_object();
    struct MHD_Response *res;
    char* key;
    json_t* value;
    int ret;
    if (NULL == *con_cls) {
        *con_cls = connection; return MHD_YES;
    }
    if (strcmp(method,"GET") != 0) {
        res = MHD_create_response_from_buffer(strlen(MSG),(void*)MSG,MHD_RESPMEM_PERSISTENT);
        MHD_queue_response(connection,MHD_HTTP_NOT_IMPLEMENTED,res);
        return MHD_YES;
    }
    mongoc_collection_t* coll = init();
    if(!coll) {
        abort();
    }
    char* data = getData(coll);
    res = MHD_create_response_from_buffer(strlen(data),(void*)data,MHD_RESPMEM_PERSISTENT);
    if (res == NULL) 
       {
           printf("[*]Failed to create response\n");
           return MHD_NO;
       }
       else {
           printf("%s[*]Response was generated\n",KRED);
           RST;
           MHD_add_response_header(res,"Content-Type","application/json; charset=utf-8");
		   return MHD_queue_response(connection,MHD_HTTP_OK,res);
        
       }

}