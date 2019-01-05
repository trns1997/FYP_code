unsigned long timer = 0;
const int pinNum = 4;
int pin[pinNum] = {A0, A1, A2, A3};
const int bufSize = 20;
int inputs[pinNum][bufSize] = {0};
int pointer, i, j = 0;
unsigned long sum,sum2 = 0;

#include <Wire.h>
#define SLAVE_ADDRESS 0x0A

union cvd{
  float val;
  byte b[4];
};
union cvd out[4] = {0};

union cvl{
  unsigned long val;
  byte b[4];
};
union cvl dcShift[4] = {0};

union cvi{
  int val;
  byte b[4];
};
union cvi raw[4] = {0};

void setup() {
  // put your setup code here, to run once:
  //Serial.begin(115200);
  pinMode(11, OUTPUT);
  timer = millis();
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
  //memcpy(idata,out[0].b,sizeof(idata)/4);
  //memcpy(idata+4,out[1].b,sizeof(idata)/4);
  //memcpy(idata+8,out[2].b,sizeof(idata)/4);
  //memcpy(idata+12,out[3].b,sizeof(idata)/4);
}

void loop() {
  // put your main code here, to run repeatedly:
  if ( (micros() - timer) > 5) {
    //Serial.println(micros()-timer);
    for (i=0;i<pinNum;i++){
    inputs[i][pointer] = analogRead(pin[i]);
    //raw[i].val = inputs[i][pointer];
    }

    //Serial.write(raw[0].b,4);
    //Serial.write(dcShift[0].b,4);
    //Serial.write(out[0].b,4);
    //Serial.write(raw[1].b,4);
    //Serial.write(dcShift[1].b,4);
    //Serial.write(out[1].b,4);
    //Serial.println(inputs[pointer]);
    if (pointer == bufSize - 1) {

      for (i=0;i<pinNum;i++){
        long temp = 0;
        for (j=0;j<bufSize; j++){
          temp += inputs[i][j];
        }
        dcShift[i].val = temp/bufSize;
        sum = 0;
        for (j=0;j<bufSize; j++){
          inputs[i][j] = inputs[i][j] - dcShift[i].val;
          sum += pow(inputs[i][j],2);
        }
        out[i].val = out[i].val*0.7+sqrt(sum/bufSize)*0.3;
      }
      pointer = -1;
    }
    pointer++;
    timer = micros();
  }
}
