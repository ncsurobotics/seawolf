#define DEBUG

#ifdef USE_LIBSEAWOLF
#include "seawolf.h"
#endif

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* A sample from the FPGA/ADC is 16 bits */
typedef int16_t adcsample;

/* Asychronous banks */
#define BANK_0 0x20000000
#define BANK_1 0x20100000
#define BANK_2 0x20200000
#define BANK_3 0x20300000

/* Channels */
#define A 0
#define B 1
#define C 2
#define D 3

/* Data source locations */
#define DATA_ADDR  (*((adcsample**)BANK_2))
#define READY_FLAG (*(((adcsample*)BANK_2) + 1))
#define RESET_FLAG (*(((adcsample*)BANK_2) + 3))

/* Input data configuration */
#define CHANNELS 4
#define SAMPLES_PER_CHANNEL (8 * 1024)
#define SAMPLES_PER_BANK    (CHANNELS * SAMPLES_PER_CHANNEL)
//#define BUFFER_SIZE_CHANNEL (1 * 1024 * 1024)
#define BUFFER_SIZE_CHANNEL (1024 * 1024 + 8192)

/* Value to trigger on */
#define TRIGGER_VALUE (short)(-128)

/* Circular buffer state */
#define READING   0x00
#define TRIGGERED 0x01
#define DONE      0x02

/* Extra number of read cyles to perform after trigger. This can be used to
   "pad" the other channels and ensure that the trigger is present in all
   channels */
#define EXTRA_READS 4

/* Specify samples to start and end dump at */
#define START_DUMP 4096
#define DUMP_SIZE  1048576
#define END_DUMP  (START_DUMP + DUMP_SIZE)

/* Dump channel buffer to CSV file */
void dump(const char* fname, adcsample* n) {
    FILE* f = fopen(fname, "w");
    for(int i = START_DUMP; i < END_DUMP; i++) {
        fprintf(f, "%.5f\n", n[i] / ((float)(1 << 15)));
        //fprintf(f, "%d\n", n[i]);
    }
    fclose(f);
}

int main(int argc, char** argv) {
#ifdef USE_LIBSEAWOLF
    Seawolf_loadConfig("seawolf.conf");
    Seawolf_init("Blackfin");
#endif
    
    adcsample* last_addr = (adcsample*) 0x00;
    adcsample* cirbuff[4];
    adcsample* outbuff;
    adcsample* temp_ptr;

    unsigned int cirbuff_offset;
    unsigned int extra_reads;
    unsigned int i;

    int state;
    bool cirbuff_full;
 
    /* Circular buffers per channel */
    cirbuff[A] = calloc(sizeof(adcsample), BUFFER_SIZE_CHANNEL);
    cirbuff[B] = calloc(sizeof(adcsample), BUFFER_SIZE_CHANNEL);
    cirbuff[C] = calloc(sizeof(adcsample), BUFFER_SIZE_CHANNEL);
    cirbuff[D] = calloc(sizeof(adcsample), BUFFER_SIZE_CHANNEL);

    /* Buffer used in linearization of circular buffers */
    outbuff = malloc(sizeof(adcsample) * BUFFER_SIZE_CHANNEL);

    while(true) {
        /* Reset state */
        state = READING;
        extra_reads = EXTRA_READS;
        cirbuff_full = false;
        cirbuff_offset = 0x00;
        RESET_FLAG = 1;

        printf("Waiting for trigger...");
        fflush(stdout);

        while(state != DONE) {
            /* Wait for the address pointer to change */
            while(DATA_ADDR == last_addr);
            last_addr = DATA_ADDR;

            /* Copy data out of the FPGA */
            memcpy(cirbuff[A] + cirbuff_offset, last_addr + (0 * SAMPLES_PER_CHANNEL), sizeof(adcsample) * SAMPLES_PER_CHANNEL);
            memcpy(cirbuff[B] + cirbuff_offset, last_addr + (1 * SAMPLES_PER_CHANNEL), sizeof(adcsample) * SAMPLES_PER_CHANNEL);
            memcpy(cirbuff[C] + cirbuff_offset, last_addr + (2 * SAMPLES_PER_CHANNEL), sizeof(adcsample) * SAMPLES_PER_CHANNEL);
            memcpy(cirbuff[D] + cirbuff_offset, last_addr + (3 * SAMPLES_PER_CHANNEL), sizeof(adcsample) * SAMPLES_PER_CHANNEL);

            /* Don't look for a trigger until the buffer has been filled */
            if(state == READING && cirbuff_full) {
                temp_ptr = cirbuff[A] + cirbuff_offset;
                for(i = 0; i < SAMPLES_PER_CHANNEL; i++) {
                    if(temp_ptr[i] > TRIGGER_VALUE ) { //|| true) {
                        printf("done\nStoring additional samples...");
                        fflush(stdout);

                        state = TRIGGERED;
                        break;
                    }
                }
            }
            
            /* Increment the offset into the circular buffer -- if we are back
               to 0 then set the buffer as filled to indicate that we have a
               full buffers worth of data */
            cirbuff_offset = (cirbuff_offset + SAMPLES_PER_CHANNEL) % BUFFER_SIZE_CHANNEL;
            if(cirbuff_offset == 0x00) {
                cirbuff_full = true;
            }

            /* Handle padding once triggered */
            if(state == TRIGGERED) {
                if(extra_reads > 0) {
                    extra_reads--;
                } else {
                    state = DONE;
                }
            }
            
            /* Tell the FPGA we are ready again */
            READY_FLAG = 1;
        }

        printf("done\nLinearizing data...");
        fflush(stdout);

        /* Linearize each buffer using a temporary buffer. Output is stored back
           into the circular buffer space */
        memcpy(outbuff, cirbuff[A] + cirbuff_offset, sizeof(adcsample) * (BUFFER_SIZE_CHANNEL - cirbuff_offset));
        memcpy(outbuff + (BUFFER_SIZE_CHANNEL - cirbuff_offset), cirbuff[A], sizeof(adcsample) * cirbuff_offset);
        memcpy(cirbuff[A], outbuff, sizeof(adcsample) * BUFFER_SIZE_CHANNEL);

        memcpy(outbuff, cirbuff[B] + cirbuff_offset, sizeof(adcsample) * (BUFFER_SIZE_CHANNEL - cirbuff_offset));
        memcpy(outbuff + (BUFFER_SIZE_CHANNEL - cirbuff_offset), cirbuff[B], sizeof(adcsample) * cirbuff_offset);
        memcpy(cirbuff[B], outbuff, sizeof(adcsample) * BUFFER_SIZE_CHANNEL);

        memcpy(outbuff, cirbuff[C] + cirbuff_offset, sizeof(adcsample) * (BUFFER_SIZE_CHANNEL - cirbuff_offset));
        memcpy(outbuff + (BUFFER_SIZE_CHANNEL - cirbuff_offset), cirbuff[C], sizeof(adcsample) * cirbuff_offset);
        memcpy(cirbuff[C], outbuff, sizeof(adcsample) * BUFFER_SIZE_CHANNEL);

        memcpy(outbuff, cirbuff[D] + cirbuff_offset, sizeof(adcsample) * (BUFFER_SIZE_CHANNEL - cirbuff_offset));
        memcpy(outbuff + (BUFFER_SIZE_CHANNEL - cirbuff_offset), cirbuff[D], sizeof(adcsample) * cirbuff_offset);
        memcpy(cirbuff[D], outbuff, sizeof(adcsample) * BUFFER_SIZE_CHANNEL);

#ifdef DEBUG
        printf("done\n");
        
        for(int i = 1; i < argc; i++) {
            switch(argv[i][0]) {
            case 'a':
                printf("Dumping channel a...");
                fflush(stdout);
                dump("a.csv", cirbuff[A]);
                printf("done\n");
                break;
            case 'b':
                printf("Dumping channel b...");
                fflush(stdout);
                dump("b.csv", cirbuff[B]);
                printf("done\n");
                break;
            case 'c':
                printf("Dumping channel c...");
                fflush(stdout);
                dump("c.csv", cirbuff[C]);
                printf("done\n");
                break;
            case 'd':
                printf("Dumping channel d...");
                fflush(stdout);
                dump("d.csv", cirbuff[D]);
                printf("done\n");
                break;
            default:
                printf("Invalid channel '%c'\n", argv[i][0]);
                break;
            }
        }
        exit(0);
#else
        /* TODO: Pass buffers through fir and then to delay calculation code */
#endif
    }

    free(cirbuff[A]);
    free(cirbuff[B]);
    free(cirbuff[C]);
    free(cirbuff[D]);
    free(outbuff);

#ifdef USE_LIBSEAWOLF
    Seawolf_close();
#endif

    return 0;
}
