#include <Wire.h>
#define SLAVE_ADDRESS 0x0A

union cvd{
  float val;
  byte b[4];
}out,out2,out3,out4;

void setup() {
  // put your setup code here, to run once:
  //Serial.begin(115200);
  pinMode(11, OUTPUT);
  out.val = 1;
  out2.val = 25.5;
  out3.val = 140.8;
  out4.val = 999.9;
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
  Serial.print("sendData: ");
  memcpy(idata,out.b,4);
  memcpy(idata+4,out2.b,4);
  memcpy(idata+8,out3.b,4);
  memcpy(idata+12,out4.b,4);
  //memcpy(idata+16,dcShift2.b,4);
  //memcpy(idata+20,out2.b,4);
  Wire.write(idata,16);
  //Serial.println(Wire.write(idata,16));
}



void loop() {
  // put your main code here, to run repeatedly:
}
