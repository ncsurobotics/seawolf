#define DEBUG

#ifdef USE_LIBSEAWOLF
#include "seawolf.h"
#endif

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <filter.h>
#include <math_bf.h>
#include <complex_bf.h>
#include "acoustics_math.h"
#include "csv_io.h"

/* A sample from the FPGA/ADC is 16 bits */
//typedef int16_t adcsample;
typedef fract16 adcsample;

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
#define BUFFER_SIZE_CHANNEL (512 * 1024)

/* Value to trigger on */
#define TRIGGER_VALUE (short)(-1100)
#define UN_FREQ 1728 				// Unnormalized Frequency to look for (1728 = 27kHz / 64kHz * 4096 samples)
#define THRESH_LEVEL 0x0120

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

/* Uglytacular global variables for the FIR filters */

//FIR Filter States
fir_state_fr16 firA;   
fir_state_fr16 firB;  
fir_state_fr16 firC;  
fir_state_fr16 firD;  
fir_state_fr16 smallFir;

//FIR Coefficients
fract16* coefs;

//FIR delay lines
fract16* delayA;
fract16* delayB;
fract16* delayC;
fract16* delayD;
fract16* delaySmallFir;

//FIR r/w pointers
fract16* rwA;
fract16* rwB;
fract16* rwC;
fract16* rwD;
fract16* rwSmallFir;


/* Dump channel buffer to CSV file */
void dump(const char* fname, adcsample* n) {
    FILE* f = fopen(fname, "w");
    for(int i = START_DUMP; i < END_DUMP; i++) {
        fprintf(f, "%.5f\n", n[i] / ((float)(1 << 15)));
        //fprintf(f, "%d\n", n[i]);
    }
    fclose(f);
}

void backendCalculate(adcsample* circbufA, adcsample* circbufB, adcsample* circbufC, adcsample* circbufD) 
{
     
}

void fir_setup()
{
    //FIR variables
    int pingFrequency;
    short unPingFrequency;
    int numTaps;
    char* fileName = "27.cof";

    /* Initialize FIR filter */
#ifdef USE_LIBSEAWOLF
    //Pull frequencies from SQL
#else
    //Pull frequencies from rear end
    pingFrequency = 27;
    unPingFrequency = 1728;
    numTaps = 613;
    
#endif

    
    //Initialize coefficients
    coefs  = calloc(sizeof(adcsample), numTaps);

    //Pull coefficients from file
    pullCoefs( coefs, fileName, numTaps );  

    //Initialize delay lines
    delayA = calloc(sizeof(adcsample), numTaps);
    delayB = calloc(sizeof(adcsample), numTaps);
    delayC = calloc(sizeof(adcsample), numTaps);
    delayD = calloc(sizeof(adcsample), numTaps);
    delaySmallFir = calloc(sizeof(adcsample), numTaps);

    //fir state macros
    fir_init(firA, coefs, delayA, numTaps, 0);
    fir_init(firB, coefs, delayB, numTaps, 0);
    fir_init(firC, coefs, delayC, numTaps, 0);
    fir_init(firD, coefs, delayD, numTaps, 0);
    fir_init(smallFir, coefs, delaySmallFir, numTaps, 0);
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
    unsigned int i, j, k;
	
    fract16 		*fftInput;
    complex_fract16 	*fftOutput;
    complex_fract16	*twiddleTable;
    complex_fract16	*tempTable;

    fract16 		*delay12;
    fract16 		*delay34;
	
    int state;
    bool cirbuff_full;

    int pDelay12;
    int pDelay34;
    

    //Setup fir filters
    fir_setup();

    twiddleTable = calloc(sizeof(complex_fract16), SAMPLES_PER_CHANNEL );
    tempTable = calloc(sizeof(complex_fract16), SAMPLES_PER_CHANNEL );
 
    /* Circular buffers per channel */
    cirbuff[A] = calloc(sizeof(adcsample), BUFFER_SIZE_CHANNEL);
    cirbuff[B] = calloc(sizeof(adcsample), BUFFER_SIZE_CHANNEL);
    cirbuff[C] = calloc(sizeof(adcsample), BUFFER_SIZE_CHANNEL);
    cirbuff[D] = calloc(sizeof(adcsample), BUFFER_SIZE_CHANNEL);

    //Correlation stuff
    delay12 = calloc(sizeof(adcsample), BUFFER_SIZE_CHANNEL);
    delay34 = calloc(sizeof(adcsample), BUFFER_SIZE_CHANNEL);

    //FFT
    fftInput  = calloc(sizeof(adcsample), SAMPLES_PER_CHANNEL);
    fftOutput = calloc(sizeof(adcsample), SAMPLES_PER_CHANNEL);

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
                /* Look for trigger value */
				/* Old code, looking for simple value out of ADC thresholding */
				/*
				for(i = 0; i < SAMPLES_PER_CHANNEL; i++) {
					if(temp_ptr[i] > TRIGGER_VALUE ) {
				        	printf("done\nStoring additional samples...");
				        	fflush(stdout);

				        	state = TRIGGERED;
				        	break;
					}
					
				}
				*/
				/* End old code */
				/* New code, take fft of data and look for predefined frequency */
				//Copy data to temporary buffer for analysis
				printf("Looking for trigger... \n" );
				memcpy( fftInput, cirbuff[A] + cirbuff_offset, sizeof(adcsample) * SAMPLES_PER_CHANNEL );

				//Output waveform data
				printf("CHANNEL A WAVE DATA \n");
				//printCSV(fftInput, SAMPLES_PER_CHANNEL);
				for(j = 0; j < SAMPLES_PER_CHANNEL; j++)
				{
					printf("%d \n", fftInput[j]);
				}
				printf("END DATA \n");
				
				//Zip data through FFT
				//twidfftrad2_fr16(twiddleTable, SAMPLES_PER_CHANNEL);
				//rfft_fr16(fftInput, fftOutput, twiddleTable, 1, SAMPLES_PER_CHANNEL, 0, 0);
				firfly(	fftInput, SAMPLES_PER_CHANNEL, &smallFir );
				
				//Threshold frequency value
				
				printf("CHANNEL A FIR DATA \n");
				//printCSV(fftInput, SAMPLES_PER_CHANNEL);
				for(j = 0; j < SAMPLES_PER_CHANNEL; j++)
				{
					printf("%d \n", fftInput[j]);
				}
				printf("END DATA \n");

				for(i = SAMPLES_PER_CHANNEL / 2; i < SAMPLES_PER_CHANNEL; i++) {
					if(fftInput[i] > TRIGGER_VALUE ) {
				        	//Change state to 'triggered'
						state = TRIGGERED;
						//Print FFT data to console for debug stuff
						break;
					}
					
				}
				
				/* End New Code */
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

/* Get FFT working first! */

	//FIR data
	firfly(cirbuff[A], BUFFER_SIZE_CHANNEL, &firA);
	firfly(cirbuff[B], BUFFER_SIZE_CHANNEL, &firB);
	firfly(cirbuff[C], BUFFER_SIZE_CHANNEL, &firC);
	firfly(cirbuff[D], BUFFER_SIZE_CHANNEL, &firD);

	//Correlation Blocks
	correlate(cirbuff[A], cirbuff[B], delay12, BUFFER_SIZE_CHANNEL);
	correlate(cirbuff[C], cirbuff[D], delay34, BUFFER_SIZE_CHANNEL);
	
	//Find maximum points of correlation blocks
	pDelay12 = findMax(delay12);
	pDelay34 = findMax(delay34);

	printf("pDelay12: %d \n", delay12);
	printf("pDelay34: %d \n", delay34);

	//Output pDelay values

        
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
