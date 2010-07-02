
/* I2C slave. Controls status lights, dropper, and torpedo. Communicates with PC */

#include <Wire.h>
#include <Servo.h>

#define DEVICE_NAME "PeriphBoard"

#define SLAVE 1

#define DROPPER_PIN 5
#define STATUS_PIN  6
#define TORPEDO_PIN 7

/* Toggle the light every 300 milliseconds when blinking */
#define BLINK_RATE 300

/* How quickly to run the dropper (milliseconds) */
#define DROPPER_RATE 500

/* How long to keep the dropper in the down position */
#define DROPPER_DOWN_TIME 300

/* Size in degrees of a dropper step */
#define DROPPER_STEP 10

/* Dropper servo angles for up and down */
#define DROPPER_UP 0
#define DROPPER_DOWN 180

/* Computed values (not to be changed) */
#define DROPPER_STEPS (((float)(DROPPER_DOWN - DROPPER_UP)) / DROPPER_STEP)
#define DROPPER_STEP_DELAY ((int)(DROPPER_RATE / DROPPER_STEPS))

#define CTRL_LIGHTS  0x01
#define CTRL_DROPPER 0x02
#define CTRL_TORPEDO 0x03

#define LIGHTS_OFF   0x00
#define LIGHTS_BLINK 0x01
#define LIGHTS_ON    0x02

#define DROPPER_LAUNCH 0x01

#define TORPEDO_LAUNCH 0x01

Servo dropper;

byte wire_data[3];
byte serial_data[4];
int i, j;

int light_function = LIGHTS_OFF;
int light_status = 0;
unsigned long last_light = 0;

int dropper_pos = DROPPER_UP;

void setup(void) {
    /* Set pin modes */
    pinMode(DROPPER_PIN, OUTPUT);
    pinMode(STATUS_PIN, OUTPUT);
    pinMode(TORPEDO_PIN, OUTPUT);

    /* Attach servo */
    dropper.attach(DROPPER_PIN);
    dropper.write(DROPPER_UP);

    /* Setup torpedo pin */
    digitalWrite(TORPEDO_PIN, LOW);

    /* Turn off light */
    digitalWrite(STATUS_PIN, LOW);

    /* Start communication to PC */
    Serial.begin(9600);
    handshakeSerial();
 
    /* Start I2C */
    Wire.begin(SLAVE);
    Wire.onReceive(send_data);
}

/* Receive RFID and depth data from master arduino */
void send_data(int n) {
    for(j = 0; j < n; j++) {
        wire_data[j] = Wire.receive();
    }
    
    Serial.write(wire_data, n);
}

void set_light(int s) {
    if(light_status == 0 && s == 1) {
        digitalWrite(STATUS_PIN, 1);
        light_status = 1;
    } else if(light_status == 1 && s == 0) {
        digitalWrite(STATUS_PIN, 0);
        light_status = 0;
    }
}

void toggle_light(void) {
    if(light_status == 0) {
        set_light(1);
    } else {
        set_light(0);
    }
}

void run_dropper(void) {
    while(dropper_pos < DROPPER_DOWN) {
        dropper_pos += DROPPER_STEP;
        if(dropper_pos > DROPPER_DOWN) {
            dropper_pos = DROPPER_DOWN;
        }

        dropper.write(dropper_pos);
        delay(DROPPER_STEP_DELAY);
    }

    delay(DROPPER_DOWN_TIME);
    dropper.write(DROPPER_UP);
}

void run_torpedo(void) {
    digitalWrite(TORPEDO_PIN, HIGH);
    delay(500);
    digitalWrite(TORPEDO_PIN, LOW);
}

void loop() {
    if(Serial.available() >= 3) {
        serial_data[0] = Serial.read();
        serial_data[1] = Serial.read();
        serial_data[2] = Serial.read();

        if(serial_data[0] != 0xFF) {
            Serial.flush();
            return;
        }

        switch(serial_data[1]) {
        case CTRL_LIGHTS:
            light_function = serial_data[2];
            break;
        case CTRL_DROPPER:
            run_dropper();
            break;
        case CTRL_TORPEDO:
            run_torpedo();
            break;
        }
    }

    switch(light_function) {
    case LIGHTS_OFF:
        set_light(0);
        break;
    case LIGHTS_ON:
        set_light(1);
        break;
    case LIGHTS_BLINK:
        if(millis() - last_light > BLINK_RATE) {
            last_light = millis();
            toggle_light();
        }
        break;
    }
}

int handshakeSerial(){
    int incomingByte;
    char incomingString[64];
    
    i = 0;

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
