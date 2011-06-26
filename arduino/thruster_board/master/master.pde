
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
#define SLAVE_1 0x10
#define SLAVE_2 0x20

/* Thrusters */
#define PORT   0
#define STAR   1
#define BOW    2
#define STERN  3
#define STRAFE 4

#define GET_BIT(v, b) (((v) >> (b)) & 1)

/* Optoisolation inverts the duty cycle and direction so we flip it before
   sending it out */
#define CONV_DIR(d) (1 - (d))
#define CONV_PWM(v) (0x200 - (v))

byte data[2];
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
    analogWrite(PWM1, CONV_PWM(0));
    analogWrite(PWM2, CONV_PWM(0));
    digitalWrite(DIRECTION1, CONV_DIR(0));
    digitalWrite(DIRECTION2, CONV_DIR(0));
    
    /* Start communication */
    Serial.begin(9600);
    handshakeSerial();
    Serial.flush();

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

    /* Invalid command byte order, flush serial buffers and continue */
    if(GET_BIT(data[0], 7)) {
        return;
    }
    
    data[1] = Serial.read();
        
    thruster_id = data[0];
    dir = GET_BIT(data[1], 6);
    value = (data[1] & 0x3F) * 8;

    /* Set local thruster values or forward request over I2C */
    switch(thruster_id) {
    case PORT:
        analogWrite(PWM1, CONV_PWM(value));
        digitalWrite(DIRECTION1, CONV_DIR(dir));
        break;

    case STAR:
        analogWrite(PWM2, CONV_PWM(value));
        digitalWrite(DIRECTION2, CONV_DIR(dir));
        break;

    case BOW:
    case STERN:
        Wire.beginTransmission(SLAVE_1);
        Wire.send(data, 2);
        Wire.endTransmission();
        break;

    case STRAFE:
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
