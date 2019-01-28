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
*/

unsigned long timer = 0;
const int pinNum = 4;
const int Rate = 1000;
int pin[pinNum] = {PA0, PA1, PA2, PA3};
const int bufSize = 20;
unsigned int pointer, i = 0;

int datum = 0;
float oldM[pinNum] = {0};
float M[pinNum] = {0};
float S[pinNum] = {0};

//unsigned long temp_timer = 0;

#include <Wire_slave.h>
#define SLAVE_ADDRESS 0x0A

union cvd{
  float val;
  byte b[4];
};
union cvd out[4] = {0};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  //pinMode(11, OUTPUT);
  timer = micros();
  for (i=0;i<pinNum;i++){
    pinMode(pin[i],INPUT_ANALOG);
  }
  Wire.begin(SLAVE_ADDRESS);
  //Wire.onReceive(receiveEvent);
  Wire.onRequest(sendData);
}

//void receiveEvent(int bytes){
//  while (Wire.available()){
//    int data = Wire.read();
//    //Serial.print("data received: ");
//    //Serial.println(data);
//  }
//}

void sendData(){
  for (i=0;i<pinNum;i++){
    Wire.write(out[i].b,4);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if ( (micros() - timer) > Rate) {
    //temp_timer = micros();
    timer = micros();
    for (i=0;i<pinNum;i++){
      datum = analogRead(pin[i]);
      oldM[i] = M[i];
      M[i] = M[i]+(datum-M[i])/(pointer+1);
      S[i] = S[i]+(datum-M[i])*(datum-oldM[i]);
    }
    if (pointer >= bufSize-1){
      for (i=0;i<pinNum;i++){
        out[i].val = sqrt(S[i]/bufSize);
        M[i] = 0;
        S[i] = 0;
      }
      pointer = -1;
    }
    pointer++;
    //Serial.println(micros()-temp_timer);
  }
}
