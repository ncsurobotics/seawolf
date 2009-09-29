#define pressure_in 0
#define numRows 2
#define numCols 16

float depthOffset;

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  handshakeSerial();
  
  //depthOffset = offset();
  depthOffset = 0;
}

float offset(){
  float pressure=0;
  int i;
  
  for(i=0;i<100;i++){
    pressure = pressure + analogRead(pressure_in);
  }
  
  pressure=pressure/100;
  
  return pressure;
}


void loop() {
  float pressure=0; 
  float depth;
  int i;
  
  for(i=0;i<1000;i++){
    pressure = (pressure + analogRead(pressure_in));
  }
  pressure=pressure/1000 - depthOffset;
  
  pressure = pressure * 25 / 1024;
  depth = pressure*.703242*3.2808399;  //depth in ft.
  
  Serial.print(depth);
  Serial.print('\n');
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
