
/* Standard includes */
#include <errno.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>

/* Networking includes */
#include <arpa/inet.h>
#include <netdb.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/time.h>

#include "seawolf/notify.h"

#define MAX_CLIENTS 128

int main(void) {
    int svr_sock = 0; /* server socket */
    int client_new = 0; /* temp place for incoming connections */
    int client_socks[MAX_CLIENTS]; /* client socket descriptors */
    const int reuse = 1; /* passed to setsockopt to allow reuse of socket */
    fd_set fdset_mask_r; /* file descriptor set passed to select call */
    char buffer[256]; /* read buffer */
    int amount_read; /* amount read from client */
    struct sockaddr_in svr_addr; /* Server binding address/port structure */
    int n; /* misc */

    /* Please *ignore* SIGPIPE. It will cause the program to close in the case
       of writing to a closed socket. We handle this ourselves. */
    signal(SIGPIPE, SIG_IGN);

    /* Clear all descriptors */
    memset(client_socks, 0, sizeof(int) * MAX_CLIENTS);

    /* Initialize the connection structure to bind the the correct port on all
       interfaces */
    svr_addr.sin_family = AF_INET;
    svr_addr.sin_addr.s_addr = 0; /* 0.0.0.0 - all interfaces */
    svr_addr.sin_port = htons(NET_PORT);
    
    /* Create the socket */
    svr_sock = socket(AF_INET, SOCK_STREAM, 0);
    if(svr_sock == -1) {
        fprintf(stderr, "Error creating socket: %s\nExiting\n", strerror(errno));
        exit(1);
    }

    /* Allow localhost address reuse. This allows us to restart the hub after it
       unexpectedly dies and leaves a stale socket */
    setsockopt(svr_sock, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse));

    /* Bind the socket to the server port/address */
    if(bind(svr_sock, (struct sockaddr*) &svr_addr, sizeof(svr_addr)) == -1) {
        fprintf(stderr, "Error binding to host: %s\nExiting\n", strerror(errno));
        exit(1);
    }

    /* Start listening */
    listen(svr_sock, MAX_CLIENTS);
    
    /* Start sending/recieving messages */
    while(true) {
        /* Zero of the file descriptor set */
        FD_ZERO(&fdset_mask_r);

        /* Add the server socket to the set */
        FD_SET(svr_sock, &fdset_mask_r);

        /* Add each client to the set */
        for(int i = 0; i < MAX_CLIENTS; i++) {
            if(client_socks[i] != 0) {
                FD_SET(client_socks[i], &fdset_mask_r);
            }
        }

        /* Perform the select call, return -1 is an error, and 0 means no
           results */
        n = select(FD_SETSIZE, &fdset_mask_r, NULL, NULL, NULL);
        if(n < 0) {
            fprintf(stderr, "Error selecting from descriptors: %s\nAttempting to continue\n", strerror(errno));
            continue;
        } else if(n == 0) {
            /* Select returned no active sockets. Ignore it and try again */
            continue;
        }

        /* If the server socket is set then a new connection is coming
           in. Handle it */
        if(FD_ISSET(svr_sock, &fdset_mask_r)) {
            client_new = accept(svr_sock, NULL, 0);
        }

        /* Check for incoming data */
        for(int i = 0; i < MAX_CLIENTS; i++) {
            if(client_socks[i] == 0 && client_new) {
                /* If client_socks[i] is 0 and client_new is non zero we have a
                   place to store the descriptor for the client connection we
                   just accepted */
                client_socks[i] = client_new;
                client_new = 0;
                printf("Accepted new client connection\n");
            } else if(client_socks[i] != 0 && FD_ISSET(client_socks[i], &fdset_mask_r)) {
                /* Read data from the client  */
                amount_read = 0;
                while(true) {
                    n = recv(client_socks[i], buffer + amount_read, 1, 0);
                    if(n == 0) {
                        /* Client has closed connection */
                        shutdown(client_socks[i], SHUT_RDWR);
                        client_socks[i] = 0;
                        break;
                    } else if(n == -1) {
                        /* Read error */
                        perror("Receive error");
                    }
                    
                    /* Increment amount_read and if we just read a null
                       character then break */
                    if(buffer[amount_read++] == '\0') {
                        break;
                    }
                }
                
                /* Socket was shut down or there was an error. Continue with
                   next socket */
                if(n == 0 || n == -1) {
                    continue;
                }

                /* Send message back out */
                for(int j = 0; j < MAX_CLIENTS; j++) {
                    if(client_socks[j]) {
                        n = send(client_socks[j], buffer, amount_read, 0);
                        if(n == -1) {
                            /* Socket failed to send data */
                            perror("Send error, shutting down client");
                            shutdown(client_socks[j], SHUT_RDWR);
                            client_socks[j] = 0;
                        }
                    }
                }
            }
        }

        /* We have a new client but we weren't able to store them anywhere. Max
           clients limit has been exceded */
        if(client_new) {
            fprintf(stderr, "Hub has excessive client count!\n");
        }
    }

    /* Shut down server socket */
    shutdown(svr_sock, SHUT_RDWR);
    return 0;
}
