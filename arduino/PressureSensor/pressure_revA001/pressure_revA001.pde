
/* The output pin (wiper) is connected to pin 3 */
#define READ_PIN 3

/* Air and water pressure constants. Varies by location (calibration recommended) */
#define PSI_PER_FOOT 0.4335
#define AIR_PRESSURE 14.23

void setup(void) {
  Serial.begin(9600);
  handshakeSerial();
}

void loop(void) {
    int val;
    float voltage, psi, depth;

    val = analogRead(READ_PIN);
    voltage = (float) val * (5.0/1024.0);
    psi = ((voltage-0.5)*100)/4.0;  
    depth = (psi-AIR_PRESSURE)/PSI_PER_FOOT;
    delay(100);
    
    Serial.println(depth);
}

int handshakeSerial(void) {
    int incomingByte;
    char incomingString[64];
    int i = 0;

    /* Wait for established message */
    while(1) {
        incomingByte = Serial.read();
        if(incomingByte == -1 || (incomingByte != '{' && i == 0)) {
            Serial.println("{ID|PressureSensor}");
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
    
    /* Sanity check */
    if(strcmp(incomingString, "{ESTABLISHED|NULL}") != 0) {
        Serial.println("Invalid message from client!");
        return 0;
    }
    
    /* Wait for {READY|NULL} message */
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
