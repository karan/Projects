
#include "services.h"
#include <stdio.h>
#include <microhttpd.h>
#include <assert.h>

int main(int argc,char* argv[]) {
	
	struct MHD_Daemon *d = MHD_start_daemon(MHD_USE_THREAD_PER_CONNECTION,4040,NULL,NULL,&handler,NULL,MHD_OPTION_END);
    assert(d);
    printf("[*]Daemon waiting on port 4040\n");
    getchar();
    MHD_stop_daemon(d);
	

	return 0;
}
