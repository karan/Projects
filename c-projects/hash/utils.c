#include <openssl/evp.h>
#include <openssl/evperr.h>
#include <string.h>
#include <libgen.h>
#include <unistd.h>
#include <ctype.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <utils.h>

// to include this help function in a utils lib for personal usage


int  main(int argc, char* argv[]) {
 
    char* msg, *filename = NULL;
    int c;
    while ((c = getopt (argc, argv, "s:f:h")) != -1)
     {
         switch(c) {
             case 's':
                printf("%s\n",getMD5(optarg));
                break;
            case 'f':
                printf("%s\n",fgetMD5(optarg));
                break;
            case 'h':
                printf("%s -s <string> -f <filename>\n",basename(argv[0]));
                break;
            case '?':
                if (optopt == 's')
                    fprintf (stderr, "Option -%c requires an argument.\n", optopt);
                else if (isprint (optopt))
                    fprintf (stderr, "Unknown option `-%c'.\n", optopt);
                else
                    fprintf (stderr,"Unknown option character `\\x%x'.\n",optopt);
                    abort();
            default:
                abort();
         }
     }
    

    return 0;
}


char* getMD5(char* message) {
    const EVP_MD* md;
    EVP_MD_CTX *mdctx;
    unsigned char md_value[EVP_MAX_MD_SIZE];
    unsigned int md_len;

    char* digest = "md5";

    md = EVP_get_digestbyname(digest);
    if (md == NULL) {
            printf("Unknown message digest %s\n",digest);
            printf("%d\n",ERR_load_EVP_strings());
            exit(1);
        }

    mdctx = EVP_MD_CTX_new();
    EVP_DigestInit_ex(mdctx, md, NULL);
    EVP_DigestUpdate(mdctx,message,strlen(message));
    
    EVP_DigestFinal_ex(mdctx, md_value, &md_len);
    EVP_MD_CTX_free(mdctx);

    
    char* c = malloc(1);
    data = malloc(md_len*2);

    for ( int i =0;i<md_len;i++) {
        sprintf(c,"%x",md_value[i]);
        strcat(data,c);   
    }   
    free(c);

    return data;
}

char* fgetMD5(char* filename) {
    struct stat st;
    if ((stat(filename,&st)) == -1)
    {
        perror("Failed stating the file");
        return NULL;
    }
    int fd = open(filename,O_RDONLY);
    char* message = malloc(st.st_size);
    message = mmap(NULL,st.st_size,PROT_READ,MAP_PRIVATE,fd,0);
    close(fd);
    return getMD5(message);

}




