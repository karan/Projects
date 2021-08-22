#include <stdio.h>
#include <bson/bson.h>
#include <mongoc/mongoc.h>
#include <string.h>
#include <stdlib.h>

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
   // mongoc_collection_destroy (coll);
   // mongoc_database_destroy (db);
   // mongoc_client_destroy (client);
  // mongoc_cleanup ();
}

char* getData( mongoc_collection_t* coll) {

    mongoc_cursor_t *cursor;
    const bson_t *doc;
    bson_error_t error;

    bson_t query = BSON_INITIALIZER;
    bson_t* opts = BCON_NEW("limit", BCON_INT32(10),"projection","{","_id",BCON_INT32(0),"}"); // need to use projection as document for the opts 

    //db.chinese.find({},{proverb:1,category:1,_id:0})  - only get category and proverb

    char *str;
    char* data = malloc(2024*sizeof(char));

    cursor = mongoc_collection_find_with_opts (coll, &query, opts, NULL);

    while (mongoc_cursor_next (cursor, &doc)) {
        
            str = bson_as_canonical_extended_json (doc, NULL);
            strcat(data,str);
            bson_free (str);
        }
     if (mongoc_cursor_error (cursor, &error)) {
        fprintf (stderr, "[*] Failed to iterate all documents: %s\n", error.message);
        return NULL;
    }

    mongoc_cursor_destroy (cursor);
    return data;

}


