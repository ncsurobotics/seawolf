
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

#define LOW_SENSE 100
#define SENSE_WAIT 100

#define RFID_EN 2
#define DEPTH_PIN 7
#define SENSE_PIN 0

/* State transitions
 *
 * RESET -> RUNNING = Receive RFID beacon 
 * RUNNING -> KILLED = Power goes from high to low
 * KILLED -> RESET = Power goes from low to high 
 */

/* States */
#define STATE_RESET   0 /* Initial state. Waiting for RFID 'beacon' */
#define STATE_RUNNING 1 /* Normal running. 24 volts is active */
#define STATE_KILLED  2 /* Killed, 24 volts is off, but nothing is reset */

/* Store data from RFID reader */
unsigned long check = 0;
unsigned long last_rfid = 0;
byte data;

/* Data from the depth sensor */
unsigned long last_depth = 0;
unsigned int depth = 0;

/* Sense information */
int sense = 0;
int last_sense_value = 0;
unsigned long last_sense_change = 0;

/* State */
int state = STATE_RUNNING;

byte wire_data[3];

int get_sense_value(void) {
    int v = analogRead(SENSE_PIN);

    if(v < LOW_SENSE) {
        return 0;
    } else {
        return 1;
    }
}

void setup(void) {
    /* Set pin mode */
    pinMode(RFID_EN, OUTPUT);

    /* Disable RFID reader */
    digitalWrite(RFID_EN, HIGH);

    /* Enable serial for RFID reader */
    Serial.begin(2400);

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

    /* Enable RFID reader */
    digitalWrite(RFID_EN, LOW);
}

void loop() {
    if(state == STATE_RESET) {
        /* Check if a data pack from the RFID reader is available */
        if(Serial.available() > 0) {
            data = Serial.read();

            /* A read from the RFID reader begins with the value 0x0A. To cut down
               on false reads, two reads must be received from the RFID reader
               within RECEIVE_THRESHOLD milliseconds. Furthermore, only one
               notification will be sent to the PC for every MIN_WAIT_TIME
               milliseconds */
            if(data == 0x0A) {
                if(millis() - check < RECEIVE_THRESHOLD) {
                    check = 0;
                    
                    wire_data[0] = 0x01;
                    wire_data[1] = 0x00;
                    wire_data[2] = 0x01;
                    
                    Wire.beginTransmission(SLAVE);
                    Wire.send(wire_data, 3);
                    Wire.endTransmission();

                    /* Switch to RUNNING state */
                    state = STATE_RUNNING;
                    last_sense_value = get_sense_value();
                    last_sense_change = millis();
                    digitalWrite(RFID_EN, HIGH);
                } else {
                    check = millis();
                }
            }
        }
    } else if(state == STATE_RUNNING) {
        /* Disable RFID Reader */
        digitalWrite(RFID_EN, HIGH);

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
        sense = get_sense_value();
        if(sense != last_sense_value && (millis() - last_sense_change) > SENSE_WAIT) {
            /* Record the change */
            last_sense_value = sense;
            last_sense_change = millis();

            /* If the transition was from high -> low then initiate a state change to killed */
            if(sense == 0) {
                wire_data[0] = 0x01;
                wire_data[1] = 0x01;
                wire_data[2] = 0x02;

                Wire.beginTransmission(SLAVE);
                Wire.send(wire_data, 3);
                Wire.endTransmission();

                state = STATE_KILLED;
            }
        }
    } else if(state == STATE_KILLED) {
        /* Check for power state change */
        sense = get_sense_value();
        if(sense != last_sense_value && (millis() - last_sense_change) > SENSE_WAIT) {
            /* Record the change */
            last_sense_value = sense;
            last_sense_change = millis();

            /* If the transition was from low -> high then initiate a state change to reset */
            if(sense == 1) {
                wire_data[0] = 0x01;
                wire_data[1] = 0x02;
                wire_data[2] = 0x00;

                Wire.beginTransmission(SLAVE);
                Wire.send(wire_data, 3);
                Wire.endTransmission();

                state = STATE_RESET;
                digitalWrite(RFID_EN, LOW);
            }
        }
    }
}
