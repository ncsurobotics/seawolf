#define BUFF_SIZE 128000
#define VAR_SIZE 16

#include <stdio.h>
#include <stdlib.h>
#include "CircularBuffer.h"

#define DATA_POINTER ((short**) 0x20200000)  //Location in memory that holds the location of where the data is.
#define DONE_FLAG ((short*) 0x20200001)  //Location in memory that we use to indicate when we're done reading data.
#define DONE_READING 1
#define DATA_READY ((short*) 0x20200002)  //Location in memory that indicates whether or not data is ready to be read.
#define RESET_FPGA ((short*) 0x20200006)  //Resets the FPGA when 1 is written to it.
#define PULL_SIZE 8192

#define THRESH_HOLD 16784

short* buffAddr;

int main(){
	int i=0;
	int index = 0;
	short data;
	
	index = fillBuffer();
	
	for(i=0;i<BUFF_SIZE;i++){
		data = readData(buffAddr,&index);
		printf("%d \n", data);
	}
	
	return 0;
	
}

//starts the circulat buffer, returns fault if we can't allocate the memory
short* cBuff() {
	short* buffAddr = 0; //stores the location of the start of the buffer
	
	buffAddr = calloc(BUFF_SIZE, VAR_SIZE);
	
	if(buffAddr == NULL)
		printf("Not enough memory.");
	
	return buffAddr;
}

/*
 *adjust to work with shorts, two per memory slot.
 */

//Gets data from the FPGA mapped as memory locations and puts them in the buffer
int fillBuffer(){
	short data = 0;
	short ready = 0;
	short* readLoc = 0;
	short i = 0;
	int index = 0;
	short window = 0;
	
	buffAddr = cBuff();
	
	while(1){
		while(ready)
			ready = *DATA_READY;
		
		//get the location of the data and start getting data
		readLoc = *DATA_POINTER;
		
		//Send data to the circular Buffer
		for(i=0;i<PULL_SIZE;i++){
			data = *(readLoc + i);
			window = windowFun(data, window);
			index = writeData(buffAddr, index, data);
		}
		
		if(window>0){
			while(ready)
				ready = *DATA_READY;
			
			//get the location of the data and start getting data
			readLoc = *DATA_POINTER;
			
			//Send data to the circular Buffer
			for(i=0;i<8192;i++){
				data = *(readLoc + i);
				index = writeData(buffAddr, index, data);
			}
			
			break;
		}
		
		
		//clear the data ready flag
		*DONE_FLAG = DONE_READING;
	}
	
	return index;
}

//retartedly simple windowing function
short windowFun(short data, short window){
	if(data > THRESH_HOLD)
		window++;
	return window;
}

void resetFPGA(){
	*RESET_FPGA = 1;
	return;
}


//Writes data to the circular buffer
short writeData(short* buffAddr, int index, short data){
	buffAddr[index] = data;
	index++;
	index = index%BUFF_SIZE;
	return index;
}

//Performs a non destructive read 
short readData(short* buffAddr, int* index){
	short data = 0;
	
	index++;
	*index = (*index)%BUFF_SIZE;
	data = buffAddr[*index];
	
	return data;
}
