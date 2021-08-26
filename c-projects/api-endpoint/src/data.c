#include <stdio.h>
#include <bson/bson.h>
#include <mongoc/mongoc.h>
#include <string.h>
#include <stdlib.h>

#define BUFF_SIZE 15000

mongoc_collection_t* init() {
    const char* URI = "mongodb://admin:admin@localhost/?authMechanism=SCRAM-SHA-1"; //should be finally exporeted as env variable for microservice usage
    mongoc_client_t *client; 
    mongoc_database_t * db;
    mongoc_collection_t * coll;

    mongoc_init ();

    client = mongoc_client_new(URI);
    if (!client) {
        abort();
    }
    db = mongoc_client_get_database(client,"proverbs");
    if (!db) {
        fprintf(stderr,"[*] Failed to get db test\n");
    }
    coll = mongoc_client_get_collection(client,"proverbs","chinese");
    if (!coll) {
        fprintf(stderr,"[*] Collection not found\n");
	return NULL;
    }
    return coll;


    // cleanup shit ( needs to be moved to calling func or to be saved to stand alone func, maybe cleanup()
    mongoc_collection_destroy (coll);
    mongoc_database_destroy (db);
    mongoc_client_destroy (client);
    mongoc_cleanup ();
}

char* getData( mongoc_collection_t* coll) {

    mongoc_cursor_t *cursor;
    const bson_t *doc;
    bson_error_t error;

    bson_t query = BSON_INITIALIZER;
    bson_t* opts = BCON_NEW("limit", BCON_INT32(128),"projection","{","_id",BCON_INT32(0),"}"); // need to use projection as document for the opts 

    //db.chinese.find({},{proverb:1,category:1,_id:0})  - only get category and proverb

    char *str;
    char* data = malloc(BUFF_SIZE*sizeof(char));
    strcpy(data,"\n[\n");

    cursor = mongoc_collection_find_with_opts (coll, &query, opts, NULL);
     size_t chunk = 0;
    long long count = 0;
    count = mongoc_collection_count(coll,MONGOC_QUERY_NONE,NULL,0,0,NULL,&error);
    if (count < 0) {
        fprintf (stderr, "%s\n", error.message);
     } else {
      printf ("%" PRId64 "\n", count);
     }
        while ( mongoc_cursor_next (cursor, &doc)) {
            str = bson_as_canonical_extended_json (doc, NULL);
            chunk += strlen(str);
            strcat(data,str);
            strcat(data,",");
            bson_free (str);
        }
        printf("%lu\n",chunk);
// need to use realloc to manually increase size of data to bring in more docs from Mongo

    
       data[strlen(data)-1] = '\0';
       strcat(data,"]\n"); // need this to have a valid JSON struct, otherwise the frontend will not pick it
     if (mongoc_cursor_error (cursor, &error)) {
        fprintf (stderr, "[*] Failed to iterate all documents: %s\n", error.message);
        return NULL;
    }

    mongoc_cursor_destroy (cursor);
    return data;

}


