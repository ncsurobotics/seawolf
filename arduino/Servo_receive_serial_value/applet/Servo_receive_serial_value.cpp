#include <Servo.h>
#define MAX_SERIAL_PARSE 4

#include "WProgram.h"
void setup();
void loop();
Servo myservo;

char incoming; // incoming serial data
char outbound[10];
int i,j,k;
int value;

void setup() {
  int i=j=k=0;
  Serial.begin(9600);
  Serial.println("Servo_Board Ready\n\n");
  Serial.println("Serial format: ###\n\t(where ### is angle between 0 and 180)\n");
  myservo.attach(9);
  
  //initialize array
  while(k<MAX_SERIAL_PARSE){
    outbound[k] = NULL;
    k++;
  }
}

void loop() {
  i=0; // reset the array index
  j=0;
  while (Serial.available() && i<3)
  {
    incoming = Serial.read();  
    if (incoming == 64) break; // escape character is @
    if ((incoming < 48) or (incoming > 57)) break; // discard non-numerics
    outbound[i]=incoming; //copy the serial byte to the array
    Serial.println(incoming);
    i++; // increase the array index
  }
  if (i != 0) {    //if the array is not zero, there is data
    outbound[i] = 0;  //last char of the array is NULL
    Serial.print("\nSending ");Serial.print(outbound);Serial.print(" to servo.\n");
    while(j<=i){
      outbound[j] -= 48;  //converting ascii to dec
      j++;
    }
    value = (outbound[0] * 100) + (outbound[1] * 10) + ((outbound[2] * 1)) ;
    if(value<0 || value>180){
      Serial.println("\nERROR out of range 0<x<180");
      return;
    }
    myservo.write(value);
    value = 0;
  }
}
  


int main(void)
{
	init();

	setup();
    
	for (;;)
		loop();
        
	return 0;
}

