/*
* Welford's method for computing variance
* sampling freq = 1kHz. According to Nyquist frequency, sampling freq ~1kHz. (EMG ~400-500Hz)
* output freq = 1k/20Hz
* source: 
* http://jonisalonen.com/2013/deriving-welfords-method-for-computing-variance/
* Input: 
* PA0 - A0 - Bicep
* PA1 - A1 - Tricep
* PA2 - A2 - Anterior
* PA3 - A3 - Posterior
* Output:
* SDA, SCL - I2C
* 
* TODO:
* DMA - DualMode - Continuous Conversion
*/


#include <Wire_slave.h>
#define SLAVE_ADDRESS 0x0A

#define DEBUG 0

unsigned long timer = 0;
const int Rate = 500;
const int pin[] = {PA0, PA1, PA2, PA3, PA4, PA5, PA6, PA7};
const int pinNum = sizeof(pin)/sizeof(int);
const int bufSize = 20;

unsigned int pointer, i = 0;
int datum = 0;
float oldM[pinNum] = {0};
float M[pinNum] = {0};
float S[pinNum] = {0};

#if DEBUG
unsigned long temp_timer = 0;
#endif

union cvd{
  float val;
  byte b[4];
};
union cvd out[pinNum] = {0};

void setup() {
  // put your setup code here, to run once:

  #if DEBUG
    Serial.begin(115200);
  #endif

  timer = micros();
  for (i=0;i<pinNum;i++){
    pinMode(pin[i],INPUT_ANALOG);
  }
  Wire.begin(SLAVE_ADDRESS);
  Wire.onRequest(sendData);
}

void sendData(){
  for (i=0;i<pinNum;i++){
    Wire.write(out[i].b,4);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if ( (micros() - timer) > Rate) {
    #if DEBUG
      temp_timer = micros();
    #endif
    timer = micros();
    for (i=0;i<pinNum/2;i++){
      datum = analogRead(pin[i]);
      oldM[i] = M[i];
      M[i] = M[i]+(datum-M[i])/(pointer+1);
      S[i] = S[i]+(datum-M[i])*(datum-oldM[i]);
    }
    for (i=pinNum/2;i<pinNum;i++){
      datum = analogRead(pin[i]);
      S[i] = S[i]+datum*datum;
    }
    
    if (pointer >= bufSize-1){
      for (i=0;i<pinNum;i++){
        out[i].val = sqrt(S[i]/bufSize);
        M[i] = 0;
        S[i] = 0;
      }
      #if DEBUG
      //Serial.println(String(out[4].val)+","+String(out[5].val));//+","+String(out[4].val)+","+String(out[5].val));
      #endif
      pointer = -1;
    }
    pointer++;
    #if DEBUG
      Serial.println(micros()-temp_timer);
    #endif
  }
}
