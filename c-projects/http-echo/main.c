
#include "http-echo.h"
#include <microhttpd.h>

/*
Just starts the HTTPD daemon, which used handler as a callback for handling requests
*/
int main() {
    struct MHD_Daemon *d = MHD_start_daemon(MHD_USE_THREAD_PER_CONNECTION,80,NULL,NULL,&handler,NULL,MHD_OPTION_END);
    assert(d);
    printf("[*]Daemon waiting on port 80\n");
    getchar();
    MHD_stop_daemon(d);
    return 0;
}




