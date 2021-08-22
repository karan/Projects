#include <bson/bson.h>
#include <mongoc/mongoc.h>

void findDoc(mongoc_collection_t*);
char* findAll(mongoc_collection_t*);
bson_error_t insertElem(mongoc_collection_t* coll,char* value);