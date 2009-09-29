#include <Servo.h>
#define SERVO_PIN 9
#define OFFSET 40    //digital servo offset.  range from 040 to 160
                      //only give it values 000 to 120
Servo dropper; //dropper servo object


void setup() {
  Serial.begin(9600);
  handshakeSerial();
  dropper.attach(SERVO_PIN);
}

void loop() {
  char incomingByte = 0;
  char serialData[4];
  int angle=0;
  int i = 0;
  
  while(Serial.available() && i<4)
  {
    incomingByte = Serial.read();
    if ((incomingByte < 48) or (incomingByte > 57)) break; // discard non-numerics
    serialData[i] = (int)incomingByte - 48; //copy the serial byte to the array and convert ASCII to dec

    //debug println
    //Serial.println(incomingByte);

    i++; // increase the array index
  }
  if( i != 0){
    angle = serialData[0]*100 + serialData[1]*10 + serialData[2]*1 ;
    angle += OFFSET;
    if(angle > 120) angle = 120;
    if(angle < 0) angle = 0;    
    dropper.write(angle);
    delay(15);
    angle=0;
  }
}
  
 
  
  
  
int handshakeSerial(){
    int incomingByte;
    int i = 0;
    char incomingString[64];

    /* Wait for established message */
    while(1){
        incomingByte = Serial.read();
        if(incomingByte == -1 || (incomingByte != '{' && i == 0)) {
            Serial.println("{ID|Dropper}");
            delay(250);
            continue;
        }
        
        incomingString[i] = incomingByte;
        incomingString[++i] = '\0';
        if(incomingByte == '}') {
            break;
        }
    }
    
    Serial.println(incomingString);

    if(strcmp(incomingString, "{ESTABLISHED|NULL}") != 0) {
        Serial.println("Invalid message from client!");
        return 0;
     }

    /* Wait for READY message */
    while(1) {
        incomingByte = Serial.read();
        if(incomingByte == -1) {
            delay(100);
        } else if(incomingByte == '}') {
            break;
        }
    }

    return 1;
}
