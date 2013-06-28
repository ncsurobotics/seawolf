
#include <Servo.h>

#define SERVO0_PIN 9
#define SERVO1_PIN 10

Servo servo0, servo1;

void set_servo(Servo s, unsigned char pos) {
    s.write(pos);
}

void setup() {
    servo0.attach(SERVO0_PIN);
    servo1.attach(SERVO1_PIN);
    set_servo(servo0, 90);
    set_servo(servo1, 90);

    Serial.begin(9600);
    handshakeSerial();
    Serial.read();  // Read extra newline at end of handshake
}

void loop() {
    if(Serial.available() >= 2) {
        unsigned char servo = Serial.read();
        unsigned char angle = Serial.read();
        if(servo == 0) {
            set_servo(servo0, angle);
        } else {
            set_servo(servo1, angle);
        }
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
            Serial.println("{ID|Peripheral}");
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
