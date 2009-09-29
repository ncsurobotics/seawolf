#include <Servo.h>

#define PWM1 9 //Defines the PWM pins
#define PWM2 10

#define DIRECTION1 8 //Defines their corresponding direction pins.
#define DIRECTION2 12

#define MAX_SERIAL_PARSE 13

  #include "WProgram.h"
void setup();
void loop();
int dir, dir2;
  int value, value2;
  int dutycycle, dutycycle2;
  char incoming; // incoming serial data
  char outbound[MAX_SERIAL_PARSE];
  int i, j, k;

void setup() {
  dir = 0;
  dir2 = 0;
  i=0;
  j=0;
  k=0;

  Serial.begin(9600);
  Serial.println("Thruster_Board_1 Ready\n\n");
  Serial.println("Serial format: ####d-####D\n\t(where d is Thruster Pin 9 direction, D is Thruster Pin 10 direction)");
  Serial.println("\tValue must be between 0 and 1024.  Direction is 1 or 0");;  
  pinMode(PWM1,OUTPUT); // Servo Pins
  pinMode(PWM2,OUTPUT);

  pinMode(DIRECTION1,OUTPUT); //Direction Pins
  pinMode(DIRECTION2,OUTPUT);
  TCCR1A = 0x00; // sets timer control bits to PWM Phase and Frequency Correct mode
  TCCR1B = 0x12; // sets timer control bits to Prescaler N = 8
  ICR1 = 0x01F4; // 2Khz

  //initialize array
  while(k<MAX_SERIAL_PARSE){
    outbound[k] = NULL;
    k++;
  }
}

void loop() {
  i=0; // reset the array index
  j=0;
  while (Serial.available())
  {
    incoming = Serial.read();  
    Serial.println(incoming);
    outbound[i]=incoming; //copy the serial byte to the array
    i++; // increase the array index
  }
  if (i != 0) {
    outbound[i]=NULL;		//last char of string is NULL
    j =0;
    Serial.println(outbound);
    Serial.print("\nThruster Pin 9 value and Pin 8 direction: \n");
    Serial.print(outbound[0]);Serial.print(outbound[1]);Serial.print(outbound[2]);Serial.print(outbound[3]);Serial.print("\n");
    Serial.print(outbound[4]);
    Serial.print("\nThruster Pin 10 value and Pin 12 direction: \n");
    Serial.print(outbound[6]);Serial.print(outbound[7]);Serial.print(outbound[8]);Serial.print(outbound[9]);Serial.print("\n");
    Serial.print(outbound[10]);

    while(j<=i){
      outbound[j]-=48;		//converting ascii to dec
      j++;
    }
//    Serial.println("Finished converting to DEC");	//debug stuff

    /*
     * serial msg format is: 1024d_1024D
     * (where d or D is direction value (1 or 0)
     * (where 1024 is max thruster output.  0 is off)
     */
    value = (outbound[0] * 1000) + (outbound[1] * 100) + (outbound[2] * 10) + (outbound[3] * 1) ;
    dir  = (outbound[4] > 0);
    //skip outbound[5] cause it should be a separator char
    value2 = (outbound[6] * 1000) + (outbound[7] * 100) + (outbound[8] * 10) + (outbound[9] * 1) ;
    dir2 = ((outbound[10]) > 0);

    
    if(value<0 || value>1024){
      Serial.println("ERROR Thruster Pin 9 value out of range 0<x<1024");
      return;
    }
    if(value2<0 || value2>1024){
      Serial.println("ERROR Thruster Pin 10 value out of range 0<x<1024");
      return;
    }

    
    Serial.println("\nSending value to thrusters...");
    dutycycle = value*1/2;
    dutycycle2 = value2*1/2;
    analogWrite(PWM2,dutycycle2);
    digitalWrite(DIRECTION1,dir);
    digitalWrite(DIRECTION2,dir2);
  }
  else return;
}
  


int main(void)
{
	init();

	setup();
    
	for (;;)
		loop();
        
	return 0;
}

