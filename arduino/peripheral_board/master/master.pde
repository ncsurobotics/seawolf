
/* I2C master. Controls depth and RFID reader */

#include <Wire.h>

/* I2C slave */
#define SLAVE 1

/* Number of milliseconds between depth reads */
#define DEPTH_SLEEP 100

#define LOW_SENSE 100
#define HIGH_SENSE 400
#define SENSE_WAIT 250

#define DEPTH_PIN 7
#define SENSE_PIN 0

/* Data from the depth sensor */
unsigned long last_depth = 0;
unsigned int depth = 0;

/* Sense information */
int sense = 0;
int last_sense_value = 0;
unsigned long last_sense_change = 0;

byte wire_data[3];

int get_sense_value(int prev_value) {
    int v = analogRead(SENSE_PIN);

    if(prev_value == 1 && v < LOW_SENSE) {
        return 0;
    } else if (prev_value == 0 && v > HIGH_SENSE) {
        return 1;
    } else {
        return prev_value;
    }
}

void setup(void) {
    /* Start I2C */
    Wire.begin();

    /* Delay before starting */
    delay(1000);

    /* Send data sync */
    wire_data[0] = 0xff;
    wire_data[1] = 0xff;
    wire_data[2] = 0xff;

    Wire.beginTransmission(SLAVE);
    Wire.send(wire_data, 3);
    Wire.endTransmission();

    /* Enable analog reference */
    analogReference(EXTERNAL);

    /* Get initial sense value */
    last_sense_value = get_sense_value(0);
}

void loop() {
    
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

    /* Check for change to the sense */
    sense = get_sense_value(last_sense_value);
    if(sense != last_sense_value && (millis() - last_sense_change) > SENSE_WAIT) {
        /* Record the change */
        last_sense_value = sense;
        last_sense_change = millis();

        if(sense == 0) {
            wire_data[0] = 0x01;
            wire_data[1] = 0x01;
            wire_data[2] = 0x00;
        } else {
            wire_data[0] = 0x01;
            wire_data[1] = 0x02;
            wire_data[2] = 0x00;
        }

        Wire.beginTransmission(SLAVE);
        Wire.send(wire_data, 3);
        Wire.endTransmission();
    }
}
