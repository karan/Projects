#include "http-echo.h"
#include <microhttpd.h>
#include <arpa/inet.h>

/*
Function used to retrieve client IP address; took me a while to find how to do that, docs suck
*/
char* getIP(struct MHD_Connection *connection) {
    const union MHD_ConnectionInfo* addr;
    struct sockaddr_in *so;
    so =  MHD_get_connection_info(connection,MHD_CONNECTION_INFO_CLIENT_ADDRESS)->client_addr; //addr = struct sockaddr** s; // GET IP from client

    char *IP = inet_ntoa(so->sin_addr); // print client IP
    return IP;
}

    