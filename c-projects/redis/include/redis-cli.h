#include <hiredis/hiredis.h>
#include <stdbool.h>

#define PORT 6379

struct Config{
    char* hostname;
    int port;
};

redisContext* init(char* hostname,int port,char*);
bool errorCheck(redisReply* );
void cleaning(redisReply* );
bool authenticate(redisContext* ,char*);
void runCommand(redisContext*,char*);
void checkConnection(redisContext* ctx);
char* getPass();
void readConfig(struct Config*);