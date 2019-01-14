unsigned long timer = 0;
//unsigned long temp_timer = 0;
const int pinNum = 4;
int pin[pinNum] = {A0, A1, A2, A3};
const int bufSize = 20;
unsigned int pointer, i = 0;

int datum = 0;
long oldM[pinNum] = {0};
long M[pinNum] = {0};
long S[pinNum] = {0};

#include <Wire.h>
#define SLAVE_ADDRESS 0x0A

union cvd{
  float val;
  byte b[4];
};
union cvd out[4] = {0};

void setup() {
  // put your setup code here, to run once:
  //Serial.begin(115200);
  pinMode(11, OUTPUT);
  timer = micros();
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(sendData);
}

void receiveEvent(int bytes){
  while (Wire.available()){
    int data = Wire.read();
    //Serial.print("data received: ");
    //Serial.println(data);
  }
}

void sendData(){
  byte idata[16];
  for (i=0;i<4;i++){
    Wire.write(out[i].b,4);
  }
}

/*
* Welford's method for computing variance
* source: http://jonisalonen.com/2013/deriving-welfords-method-for-computing-variance/
*/

void loop() {
  // put your main code here, to run repeatedly:
  if ( (micros() - timer) > 1000) {
    //temp_timer = micros();
    timer = micros();
    for (i=0;i<pinNum;i++){
      datum = analogRead(pin[i]);
      oldM[i] = M[i];
      M[i] = M[i]+(datum-M[i])/(pointer+1);
      S[i] = S[i]+(datum-M[i])*(datum-oldM[i]);
    }
    if (pointer > bufSize-1){
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
