int analogPin = 3;     // potentiometer wiper (middle terminal) connected to analog pin 3
                       // outside leads to ground and +5V
int val = 0;           // variable to store the value read
float voltage = 0;
float psi = 0;
float depth = 0;


//These are varbiable depending on your location, weather, and purity of water!!!
float PSI_PER_FOOT = 0.4335;
float AIR_PRESSURE = 14.23;


void setup()
{
  Serial.begin(9600);          //  setup serial
  handshakeSerial();
}

void loop()
{
  val = analogRead(analogPin);    // read the input pin
  voltage = (float)val*(5.0/1024.0);
  psi = ((voltage-0.5)*100)/4.0;  
  depth = (psi-AIR_PRESSURE)/PSI_PER_FOOT;
  
  Serial.println(depth);             // debug value
}






//Handshake option
int handshakeSerial()
{
    int incomingByte;
    int i = 0;
    char incomingString[64];

    /* Wait for established message */
    while(1){
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

