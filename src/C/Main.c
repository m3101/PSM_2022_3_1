/*
    DSP Host - LTI Audio Filtering Application
    Copyright (C) 2023 Amélia O. F. da Silva

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

#define CHUNK 4096
#define FSIZE 100

#include <pulse/pulseaudio.h>
#include <pulse/simple.h>
#include "FilterUtils.h"
#include <stdio.h>
#include <stdlib.h>
#include <poll.h>
#include <unistd.h>
#include <pthread.h>
#include <signal.h>
#include <sys/stat.h>
#include <sys/signalfd.h>
#include <sys/types.h>
#include <fcntl.h>

// These will be on the heap, so they're accessible from both threads.
// We don't have to worry about race conditions because
// we'll use a simple swap technique and one thread exclusively
// reads whilst the other exclusively writes to the pointer.
float *coefs;
float *coefs_tmp;
char* pipe_path;

void* monitor_socket()
{
    //Setting up clean signal interruption
    sigset_t mask;
    sigemptyset(&mask);
    sigaddset(&mask, SIGINT);
    sigprocmask(SIG_BLOCK, &mask, NULL);

    struct pollfd polls[2];
    polls[0].fd = signalfd(-1, &mask, 0);
    polls[0].events = POLLIN;

    // Pipe
    printf("Opening pipe and awaiting connection...\n");
    polls[1].fd = mkfifo(pipe_path,__O_DIRECT);
    polls[1].events = POLLIN;

    for(;;)
    {
        poll(polls,1,0);
        if(polls[0].revents&&POLLIN) break; // SIGINT
        if(polls[1].revents&&POLLIN) //Pipe update
        {
            read(polls[1].fd,coefs_tmp,sizeof(coefs_tmp));
            float *swp = coefs;
            coefs=coefs_tmp;
            coefs_tmp=swp;
        }
    }

    printf("Closing FIFO\n");
    close(polls[1].fd);

    return 0;
}

int main(int argn, char** argv)
{
    pipe_path=getenv("PSM_PIPE");
    if(pipe_path==0)
    {
        printf("Environment variable \"PSM_PIPE\" is not defined.\n");
        return -1;
    }
    
    pa_simple *outs=0;
    pa_simple *ins=0;
    pa_sample_spec ss;
    Filter* f = 0;

    // Filter setup
    coefs=calloc(FSIZE,sizeof(float));
    coefs[0]=1;
    coefs_tmp=calloc(FSIZE,sizeof(float));
    f = filter_c(coefs,NULL,FSIZE);

    pthread_t socket_thread;
    pthread_create(&socket_thread,NULL,monitor_socket,NULL);

    
    // Setting up pulseAudio connectors
    ss.format = PA_SAMPLE_FLOAT32NE;
    ss.channels = 1;
    ss.rate = 44100;

    ins = pa_simple_new(
        NULL,
        "DSP Host Input",
        PA_STREAM_RECORD,
        NULL,
        "Audio Filtering host",
        &ss,
        NULL,
        NULL,
        NULL
    );
    outs = pa_simple_new(
        NULL,
        "DSP Host Output",
        PA_STREAM_PLAYBACK,
        NULL,
        "Audio Filtering host",
        &ss,
        NULL,
        NULL,
        NULL
    );
    if(ins==0 || outs==0)
    {
        printf("Couldn't open streams.\n");
        goto cleanup;
    }

    // Keyboard polling
    struct pollfd key;
    key.fd = STDIN_FILENO;
    key.events = POLLIN;

    printf("Feed any data into STDIN to exit.\n");

    // Main loop
    int err;
    float in[CHUNK];
    float out[CHUNK];
    for(;;)
    {
        poll(&key,1,0);
        if(key.revents&POLLIN)
        {
            printf("Exiting main loop.\n");
            break;
        }
        if(pa_simple_read(ins,in,CHUNK*sizeof(float),&err)==0)
        {
            for(unsigned short i=0;i<CHUNK;i++)
                out[i]=applyFIR(f,in[i]);
            pa_simple_write(outs,out,CHUNK*sizeof(float),&err);
        }
        else
        {
            printf("Error reading from stream: %s\n",pa_strerror(err));
            break;
        }
    }

    // Stop the socket monitor
    pthread_kill(socket_thread, SIGINT);

    cleanup:
    printf("Cleaning up...\n");
    if(outs!=0)pa_simple_free(outs);
    if(ins!=0)pa_simple_free(ins);
    if(f!=0)free_filter(&f);
    if(coefs!=0)free(coefs);
    if(coefs_tmp!=0)free(coefs_tmp);
    return 0;
}