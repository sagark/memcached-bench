#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <time.h>

#include <mach/clock.h>
#include <mach/mach.h>
#include <stdlib.h>
#include <netdb.h>

// memcached defines
#define MAGIC_NUM        0x80
#define MAGIC_NUM_OFFSET 0
#define GET_OPCODE       0x00
#define OPCODE_OFFSET    1

//#define DEBUG_PRINTS 0


#include <mach/mach_time.h>

double conversion_factor;

void Init() {
  mach_timebase_info_data_t timebase;
  mach_timebase_info(&timebase);
  conversion_factor = (double)timebase.numer / (double)timebase.denom;
}

int init_sock() {
    int sockfd;
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        printf("ERR\n");
        exit(0);
    }
    return sockfd;
}

int verify_response(char * result_packet, char * expected_value) {
    int a = strlen(expected_value);
    for (int b = 0; b < a; b++) {
        if (result_packet[36+b] != expected_value[b]) {
            printf("%c vs %c\n", result_packet[36+b], expected_value[b]);
            return 0;
        }

    }
    return 1;
}


uint64_t do_get_request(char* request_key, char* expected_value, int sockfd, struct sockaddr_in * servaddr, int reqno) {
    uint8_t requestpack[32 + strlen(request_key)];
    uint16_t swap_bytes;


    swap_bytes = strlen(request_key) << 8 | ((strlen(request_key) >> 8) & 0xFF);

    for (int i = 0; i < 32; i++) {
        requestpack[i] = 0x00;
    }

    requestpack[5] = reqno;

    requestpack[MAGIC_NUM_OFFSET+8] = MAGIC_NUM;
    requestpack[OPCODE_OFFSET+8] = GET_OPCODE;
    *((uint16_t*)requestpack+1+4) = swap_bytes;
    *((uint16_t*)requestpack+5+4) = swap_bytes;

    for (int i = 0; i < strlen(request_key); i++) {
        requestpack[32+i] = request_key[i];
    }

#ifdef DEBUG_PRINTS
    for (int i = 0; i < 32+strlen(request_key); i++) {
        if (i % 4 == 0) {
            printf("\n");
        }
        if (requestpack[i] == 'a') {
            printf("INDEX: %d\n", i);
        }
        printf("%x ", requestpack[i]);
    }
#endif

    int n;    
    char recvline[1000];


    // start timer
uint64_t t1, t2;

  Init();

  t1 = mach_absolute_time();
    if (sendto(sockfd, (char*)requestpack, 32+strlen(request_key), 0, (struct sockaddr *)servaddr, sizeof(*servaddr)) < 0) {
            perror("sendto failed");
            return 0;
    }
   
    n=recvfrom(sockfd,recvline,10000,0,NULL,NULL);

    // end timer

t2 = mach_absolute_time();

  double duration_ns = (double)(t2 - t1) * conversion_factor;  
  uint64_t duration_us;

#ifdef DEBUG_PRINTS
    for (int i = 0; i < 64; i++) {
        if (i % 4 == 0) {
            printf("\n");
        }
 
        printf("%c ", 0xFF & recvline[i]);
    }
#endif
    if (!verify_response(recvline, expected_value)) {
        printf("VERIFY FAIL");
        exit(0);
    }
    duration_us = (uint64_t) (duration_ns / 1000);
    return duration_us;
}


int main(int argc, char *argv[])
{

char* host = "127.0.0.1";
//char* host = "172.16.1.2";

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

uint64_t sum_latency_software = 0;
uint64_t sum_latency_hardware = 0;
uint64_t rounds = 20000;

/*void fill_string (char* buf, int n) {
    
*/

char key[300];
char value[2000];
unsigned int IAtime;
uint64_t latency;

for (int i = 0; i < rounds; i++) {
    //printf("round # %llu \n", i);
    //uint64_t result = 
    gets(key);
    printf("%s\n", key);
    gets(value);
    printf("%s\n", value);
    scanf("%d\n", &IAtime);
    printf("%u\n", IAtime);
    latency = do_get_request(key, value, sockfd, &servaddr, 1);
    printf("%d: %llu\n", i, latency);
    usleep((useconds_t) IAtime);
}

//printf("rounds: %llu\n", rounds);
//printf("sum_latency_software: %llu\n", sum_latency_software);
//printf("hardware avg: %f\n", ((double)sum_latency_hardware) / ((double) rounds));
//printf("software avg: %f\n", ((double)sum_latency_software) / ((double) rounds));

return 0;
}


