
/*
 * Arduinos,
 * - Master on I2C bus controls port and starboard x thrusters
 * - Slave 1 controls port and starboard y thrusters
 * - Slave 2 controls aft thruster
 */

#include <Wire.h>

#define DEVICE_NAME "ThrusterBoard"

#define PWM1 9
#define PWM2 10

#define DIRECTION1 11
#define DIRECTION2 12

/* I2C slaves */
#define SLAVE_1 1
#define SLAVE_2 2

/* Thrusters */
#define PORT_X 0
#define STAR_X 1
#define PORT_Y 2
#define STAR_Y 3
#define AFT    4

#define GET_BIT(v, b) ((v) >> (b)) & 1)

unsigned byte data[2];
unsigned int thruster_id, dir, value;

void setup(void) {
    /* Set pin modes */
    pinMode(PWM1, OUTPUT);
    pinMode(PWM2, OUTPUT);
    pinMode(DIRECTION1, OUTPUT);
    pinMode(DIRECTION2, OUTPUT);

    /* Configure PWM timers */
    TCCR1A = 0x00;      /* sets timer control bits to PWM Phase and Frequency Correct mode */
    TCCR1B = 0x12;      /* sets timer control bits to Prescaler N = 8 */
    ICR1 = 0x01F4;      /* 2Khz */

    /* Zero thrusters */
    analogWrite(PWM1, 0);
    analogWrite(PWM2, 0);
    digitalWrite(DIRECTION1, 0);
    digitalWrite(DIRECTION2, 0);
    
    /* Start communication */
    Serial.begin(9600);
    handshakeSerial();

    /* Start I2C */
    Wire.begin();
}

void loop() {
    /* Wait for full command to be available */
    if(Serial.available() < 2) {
        return;
    }

    /* Read command bytes */
    data[0] = Serial.read();
    data[1] = Serial.read();

    /* Invalid command byte order, flush serial buffers and continue */
    if(GET_BIT(data[0], 7)) {
        Serial.flush();
        return;
    }
    
    thruster_id = data[0];
    if(thruster_id == 0 || thruster_id == 1) {

    }

    dir = GET_BIT(data[1], 6);
    value = (data[1] & 0x3F) * 4; /* This was 8 in the old code, not sure
                                            why but keep it in mind if there are
                                            any problems */

    /* Set local thruster values or forward request over I2C */
    switch(thruster_id) {
    case PORT_X:
        analogWrite(PWM1, value);
        digitalWrite(DIRECTION1, dir);
        break;

    case STAR_Y:
        analogWrite(PWM2, value);
        digitalWrite(DIRECTION2, dir);
        break;

    case PORT_Y:
    case STAR_Y:
        Wire.beginTransmission(SLAVE_1);
        Wire.send(data, 2);
        Wire.endTransmission();
        break;

    case AFT:
        Wire.beginTransmission(SLAVE_2);
        Wire.send(data, 2);
        Wire.endTransmission();
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
            Serial.println("{ID|" DEVICE_NAME "}");
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
