#include <bson/bson.h>
#include <stdio.h>

int main() {
	
	bson_t* d;
	d = BCON_NEW("{" ,"}" ,"," ,"{" ,"_id" ,BCON_INT32(0), "}");
	char* data;
	data = bson_as_canonical_extended_json(d,NULL);
	printf("%s\n",data);
	bson_free(data);
	bson_destroy(d);
	
	return 0;
}
