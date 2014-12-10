#include<libmemcached/memcached.h>

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <libmemcached/memcached.h>

#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>

// memcached defines
#define MAGIC_NUM        0x80
#define MAGIC_NUM_OFFSET 0
#define GET_OPCODE       0x00
#define OPCODE_OFFSET    1

//#define DEBUG_PRINTS 0

int init_sock() {
    int sockfd;
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        printf("ERR\n");
        exit(0);
    }
    return sockfd;
}



int do_get_request(char* request_key, char* expected_value, int sockfd, struct sockaddr_in * servaddr, int reqno) {
    uint8_t requestpack[32 + strlen(request_key)];
    uint16_t swap_bytes;

    swap_bytes = strlen(request_key) << 8 | ((strlen(request_key) >> 8) & 0xFF);

    for (int i = 0; i < 32; i++) {
        requestpack[i] = 0x00;
    }

    requestpack[5] = reqno;

    requestpack[MAGIC_NUM_OFFSET+8] = MAGIC_NUM;
    requestpack[OPCODE_OFFSET+8] = GET_OPCODE;
    *((uint16_t*)requestpack+1+4) =  swap_bytes;

    *((uint16_t*)requestpack+5+4) = swap_bytes;


    for (int i = 0; i < strlen(request_key); i++) {
        requestpack[32+i] = request_key[i];
    }

#ifdef DEBUG_PRINTS
    for (int i = 0; i < 32+strlen(request_key); i++) {
        if (i % 4 == 0) {
            printf("\n");
        }
 
        printf("%x ", requestpack[i]);
    }
#endif

    int n;    
    char recvline[1000];

    /* send a message to the server */
    struct timeval time1;
    struct timeval time2;
    gettimeofday(&time1, NULL);
    if (sendto(sockfd, (char*)requestpack, 32+strlen(request_key), 0, (struct sockaddr *)servaddr, sizeof(*servaddr)) < 0) {
            perror("sendto failed");
            return 0;
    }
   
    n=recvfrom(sockfd,recvline,10000,0,NULL,NULL);
    gettimeofday(&time2, NULL);

    printf("\nrecvd\n");

#ifdef DEBUG_PRINTS
    for (int i = 0; i < 32; i++) {
        if (i % 4 == 0) {
            printf("\n");
        }
 
        printf("%x ", 0xFF & recvline[i]);
    }
#endif

    printf("time:\n");
    uint64_t diff = time2.tv_usec - time1.tv_usec;
    printf("%llu\n", diff);
}


int main(int argc, char *argv[])
{

//char* host = "127.0.0.1";
char* host = "172.16.1.2";

struct hostent *hp;     /* host information */
struct sockaddr_in servaddr;    /* server address */

memset((char*)&servaddr, 0, sizeof(servaddr));
servaddr.sin_family = AF_INET;
servaddr.sin_port = htons(11211);

/* look up the address of the server given its name */
hp = gethostbyname(host);
if (!hp) {
        fprintf(stderr, "could not obtain address of %s\n", host);
            return 0;
}

/* put the host's address into the server address structure */
memcpy((void *)&servaddr.sin_addr, hp->h_addr_list[0], hp->h_length);

int sockfd = init_sock();

uint64_t sum_latency;
uint64_t rounds = 200;


for (int i = 0; i < rounds; i++) {
    do_get_request("key_a", "asdf", sockfd, &servaddr, 1);
//    do_get_request("key_b", "asdf", sockfd, &servaddr, 1);
}



  return 0;
}


