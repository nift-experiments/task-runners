#define _GNU_SOURCE
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <time.h>
#include <string.h>
static void event(const char *id,const char *kind){char b[300];struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);int n=snprintf(b,sizeof b,"{\"task\":\"%s\",\"event\":\"%s\",\"time_ns\":%lld,\"pid\":%ld}\n",id,kind,(long long)t.tv_sec*1000000000+t.tv_nsec,(long)getpid());int fd=open("trace.jsonl",O_CREAT|O_WRONLY|O_APPEND,0600);if(fd<0||write(fd,b,n)!=n)exit(125);close(fd);}
int main(int argc,char **argv){if(argc!=2)return 125;char p[240];const char *id=argv[1];if(strlen(id)>100)return 125;event(id,"start");snprintf(p,sizeof p,"inputs/%s.json",id);FILE*f=fopen(p,"rb");if(!f)return 126;uint64_t h=14695981039346656037ULL;int c;while((c=fgetc(f))!=EOF){h^=(unsigned char)c;h*=1099511628211ULL;}fclose(f);snprintf(p,sizeof p,"out/%s.json",id);f=fopen(p,"w");if(!f)return 126;fprintf(f,"%llu\n",(unsigned long long)h);fclose(f);event(id,"complete");return 0;}
