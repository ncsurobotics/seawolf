#include <SoftwareSerial.h>

//SoftwareSerial Rx and Tx Pins
#define rxPin 2
#define txPin 3

//RFID control pins
#define enablePin 7
#define transmitPin 8

//RFID mission status codes
#define rfidStart 0xBA
#define rfidStop 0xAB

//LED Pins
#define green 13
#define blue 12

//blink status's
#define blink 1000
#define solid 1

//status variables
int statusBitOne = 0;
int statusBitTwo = 0;
int blinkStatusGreen = 0;
int blinkStatusBlue = 0;

//Setup new Softserial Port -- Note: Tx Pin does not connect to anything
SoftwareSerial rfid_io =  SoftwareSerial(rxPin, txPin);

//Counter variables
int greenCounter = 0;
int blueCounter = 0;

//Incomming data from seial port
byte incomingData;
byte missionCode[10];

void setup() 
{
  // define pin modes for tx, rx:
  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);

  //Set the RFID control pins
  pinMode(enablePin, OUTPUT);
  pinMode(transmitPin, INPUT);
  
  //Set the LED pins
  pinMode(green, OUTPUT);
  pinMode(blue, OUTPUT);

  digitalWrite(enablePin, HIGH);   // sets the enable pin HIGH (active low)
  Serial.begin(9600);
  rfid_io.begin(2400);
  
  getMission(); //get the missions ID from the RFID reader, starts SeaWolf
  
  delay(500);
  
 // handshakeSerial();
}

//Main Program loop
void loop() 
{
  int i = 0;
  int statusLight = 0;
  int statusBitOne = 0;
  int statusBitTwo = 0;
  
  Serial.println("test2");
  
  statusLight = Serial.read();
  if(statusLight != 0){
    statusBitTwo = statusLight & 0x0F;
    statusBitOne = (statusLight >> 4) & 0x0F; 
  }
  
  setStatus();
  setLights();
  
  //used for debugging prints out the RFID
  /*for(i=0;i<10;i++){
    Serial.write(missionCode[i]);
  }*/
}

//Read the Mission Code from the RFID Reader
void getMission()
{
  int i = 0;
  
  digitalWrite(enablePin, LOW); //get the RFID reader, reading
  incomingData = rfid_io.read(); //read in some data
  
  //if it's 0x0A then we've hit the beginning of the string.
  if(incomingData == 0x0A){
    for(i=0; i<10; i++){
      missionCode[i] = rfid_io.read();  //read the mission ID from the RFID reader and store it.
    }
  }
  
  Serial.write(rfidStart); //output the "hey everything happy, start doing work" message.
  
  digitalWrite(enablePin, HIGH);  //turn off the RFID reader
}

void setStatus()
{ 
  int blinkCounter;
  if(statusBitOne == 1){
    if(statusBitTwo == 1){
      blinkStatusGreen = blink;
    }
    else{
      blinkStatusGreen = solid;
    }
  }
  
  if(statusBitOne == 2){
       if(statusBitTwo == 1){
      blinkStatusBlue = blink;
    }
    else{
      blinkStatusBlue = solid;
    }
  }
}

void setLights()
{
  greenCounter++;
  blueCounter++;
  
  greenCounter = greenCounter%blinkStatusGreen;
  blueCounter = blueCounter%blinkStatusBlue;
  
  if(greenCounter < blink/2){
    digitalWrite(green, HIGH);
  }
  else{
    digitalWrite(green, LOW);
  }
  
  if(blueCounter < blink/2){
    digitalWrite(blue, HIGH);
  }
  else{
    digitalWrite(blue, LOW);
  }
}


//Handshake option
int handshakeSerial()
{
    int incomingByte;
    int i = 0;
    char incomingString[64];

    /* Wait for established message */
    while(1){
        incomingByte = Serial.read();
        if(incomingByte == -1 || (incomingByte != '{' && i == 0)) {
            Serial.println("{ID|MissionStatus}");
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
