#include "http-echo.h"


int getHeader(void *cls, enum MHD_ValueKind kind, const char *key, const char *value) {
   int res = json_object_set((json_t*)cls,key,json_string(value));
   return MHD_YES;
}


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
    char* ClientIP = getIP(connection);
    printf("[*]Received connection from: %s\n",ClientIP);
       
    MHD_get_connection_values(connection,MHD_HEADER_KIND,&getHeader,(void*)headers); // get headers; uses getHeader as callback function
            
    printf("\n%sSending Headers:",KBLU);
    RST;
    json_object_foreach(headers,key, value) {
         printf("%s : %s\n",key,json_string_value(value));
    }
    printf("\n");
    char* data = json_dumps(headers,JSON_COMPACT);
       
    json_decref((json_t*)cls);
       
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
