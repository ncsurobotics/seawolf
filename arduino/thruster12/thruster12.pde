#define PWM1 9 //Defines the PWM pins
#define PWM2 10

#define DIRECTION1 8 //Defines their corresponding direction pins.
#define DIRECTION2 11

#define RESET1 12 //reset lines on the h-bridges
#define RESET2 13

int dir = 0;    //variable 
int dutycycle = 0;

int incomingData;
int thrusterNumber;

void setup() {
  pinMode(PWM1,OUTPUT);  // Servo Pins
  pinMode(PWM2,OUTPUT);
  
  pinMode(RESET1, OUTPUT); // H-Bridge Reset lines, tie 'em high 
  pinMode(RESET2, OUTPUT);
  
  pinMode(DIRECTION1,OUTPUT); //Direction Pins
  pinMode(DIRECTION2,OUTPUT);
  
  digitalWrite(RESET1, HIGH);
  digitalWrite(RESET2, HIGH);
  
  Serial.begin(9600);
  
  handshakeSerial();
  
  TCCR1A = 0x00;      // sets timer control bits to PWM Phase and Frequency Correct mode
  TCCR1B = 0x12;      // sets timer control bits to Prescaler N = 8
  ICR1 = 0x01F4;      // 2Khz

  analogWrite(PWM1,dutycycle);
  analogWrite(PWM2,dutycycle);
}

void loop() {
  incomingData = Serial.read();
  
  if(incomingData == -1){
    return;
  }

  thrusterNumber = ((incomingData >> 7) & 1);
  dir = ((incomingData >> 6) & 1);
  dutycycle = (incomingData & B00111111) * 8;
  
  if(thrusterNumber == 0){
    analogWrite(PWM1,dutycycle);
    digitalWrite(DIRECTION1,dir);
  }
  
  if(thrusterNumber == 1){
    analogWrite(PWM2,dutycycle);
    digitalWrite(DIRECTION2,dir);
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
            Serial.println("{ID|Thruster12}");
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
