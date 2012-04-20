
#define DEPTH_PIN 0
#define DEPTH_SLEEP 100

unsigned long last_depth = 0;
unsigned int depth = 0;
byte wire_data[3];

void setup() {
    Serial.begin(9600);
    handshakeSerial();
}

void loop() {

    /* Send new depth value */
    if(millis() - last_depth > DEPTH_SLEEP) {
        last_depth = millis();
        depth = analogRead(DEPTH_PIN);

        wire_data[0] = 0x01;
        wire_data[1] = depth / 256; /* High bit */
        wire_data[2] = depth % 256; /* Low bit */

        Serial.write(wire_data, 3);
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
            Serial.println("{ID|Depth}");
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
