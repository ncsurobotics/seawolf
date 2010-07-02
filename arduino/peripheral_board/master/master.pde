
/* I2C master. Controls depth and RFID reader */

#include <Wire.h>

/* I2C slave */
#define SLAVE 1

/* To discard any misreads on the RFID reader, require two reads within this
   many milliseconds */
#define RECEIVE_THRESHOLD 500

/* Minimum number of milliseconds between accepted RFID reads */
#define MIN_WAIT_TIME 1000

/* Number of milliseconds between depth reads */
#define DEPTH_SLEEP 100

#define RFID_EN 5
#define DEPTH_PIN 0

/* Store data from RFID reader */
unsigned long check = 0;
unsigned long last_rfid = 0;
byte data;

unsigned long last_depth = 0;
unsigned int depth = 0;

byte wire_data[3];

void setup(void) {
    /* Set pin mode */
    pinMode(RFID_EN, OUTPUT);

    /* Disable RFID reader */
    digitalWrite(RFID_EN, HIGH);

    /* Enable serial for RFID reader */
    Serial.begin(2400);

    /* Start I2C */
    Wire.begin();

    /* Enable RFID reader */
    digitalWrite(RFID_EN, LOW);
}

void loop() {
    /* Check if a data pack from the RFID reader is available */
    if(Serial.available() > 0) {
        data = Serial.read();

        /* A read from the RFID reader begins with the value 0x0A. To cut down
           on false reads, two reads must be received from the RFID reader
           within RECEIVE_THRESHOLD milliseconds. Furthermore, only one
           notification will be sent to the PC for every MIN_WAIT_TIME
           milliseconds */
        if(data == 0x0A) {
            if(check == 0) {
                check = millis();
            } else if(millis() - check < RECEIVE_THRESHOLD) {
                if(last_rfid == 0 || millis() - last_rfid > MIN_WAIT_TIME) {
                    last_rfid = millis();
                    check = 0;
                    
                    wire_data[0] = 0x01;
                    
                    Wire.beginTransmission(SLAVE);
                    Wire.send(wire_data[0]);
                    Wire.endTransmission();
                }                    
            } else {
                check = millis();
            }
        }
    }

    /* Send new depth value */
    if(millis() - last_depth > DEPTH_SLEEP) {
        last_depth = millis();
        depth = analogRead(DEPTH_PIN);

        wire_data[0] = 0x02;
        wire_data[1] = depth / 256; /* High bit */
        wire_data[2] = depth % 256; /* Low bit */

        Wire.beginTransmission(SLAVE);
        Wire.send(wire_data, 3);
        Wire.endTransmission();
    }
}
