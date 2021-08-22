#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "main.h"

int main(int argc,char* argv[]) {
    const char *uri_string = "mongodb://admin:admin@localhost/?authMechanism=SCRAM-SHA-1";
    mongoc_init ();
    mongoc_client_t *client;
    mongoc_database_t * db;
    mongoc_collection_t * coll;
    bson_error_t error;
    bson_t *command;
    bson_t reply;
    bool ret;
    char* str;
    client = mongoc_client_new(uri_string);
    if (!client) {
        abort();
    }
    printf("[*] Got client connection to db\n");
    db = mongoc_client_get_database(client,"test");
    if (!db) {
        fprintf(stderr,"Failed to get db test\n");
    }
    coll = mongoc_client_get_collection(client,"proverbs","chinese");
    if (!coll) {
        fprintf(stderr,"coll not found\n");
    }
    else {
        printf("Got collection\n");
    }

    command = BCON_NEW ("ping", BCON_INT32 (1));
    ret = mongoc_client_command_simple (client, "admin", command, NULL, &reply, &error);
    if (!ret) {
        fprintf(stderr,"%s\n",error.message);
    }
    str = bson_as_json (&reply, NULL);
    printf("%s\n",str);
    char* entries[] =  findAll(coll);
    
    

    bson_destroy (&reply);
    bson_destroy (command);
    bson_free (str);


    mongoc_collection_destroy (coll);
    mongoc_database_destroy (db);
    mongoc_client_destroy (client);
    mongoc_cleanup ();

   return 0;
}
void findDoc(mongoc_collection_t* coll) {
    bson_t * query;
    query = bson_new ();
    const bson_t *doc;
    char* data;
    BSON_APPEND_UTF8 (query, "username", "j0rdan0");
    mongoc_cursor_t* cursor = mongoc_collection_find_with_opts (coll, query, NULL, NULL);

    while (mongoc_cursor_next (cursor, &doc)) {
        data = bson_as_canonical_extended_json (doc, NULL);
        printf ("%s\n", data);
        bson_free (data);
    }
        bson_destroy (query);
        mongoc_cursor_destroy (cursor);
}

void findAll(mongoc_collection_t* coll) {
    mongoc_cursor_t *cursor;
    const bson_t *doc;
    bson_error_t error;
    bson_t query = BSON_INITIALIZER;
    char *str;

    cursor = mongoc_collection_find_with_opts (coll, &query, NULL, NULL);

    while (mongoc_cursor_next (cursor, &doc)) {
    
        str = bson_as_canonical_extended_json (doc, NULL);

        printf ("%s\n", str);
        bson_free (str);
    }

    if (mongoc_cursor_error (cursor, &error)) {
        fprintf (stderr, "Failed to iterate all documents: %s\n", error.message);
    }

    mongoc_cursor_destroy (cursor);

}
bson_error_t insertElem(mongoc_collection_t* coll,char* value) {
    bson_oid_t oid;
    bson_error_t error;
    bson_t *doc = bson_new ();
    bson_oid_init (&oid, NULL);
    BSON_APPEND_OID (doc, "_id", &oid);
    BSON_APPEND_UTF8 (doc, "username", value);
    if (!mongoc_collection_insert_one (coll, doc, NULL, NULL, &error)) {
        return error;
    }
    bson_destroy (doc);
    return error;
       
}
