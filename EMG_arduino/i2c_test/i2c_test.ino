#include <Wire.h>

#define SLAVE_ADDRESS 0x0A
int data = 0;

union cvd{
  float val;
  byte b[4];
}out,out2;

union cvl{
  unsigned long val;
  byte b[4];
}dcShift,dcShift2;

union cvi{
  int val;
  byte b[4];
}raw,raw2;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(sendData);
  out.val = 50.55;
  out2.val = 60.55;
  dcShift.val = 500;
  dcShift.val = 600;
  raw.val = 50;
  raw2.val= 60;
}

void receiveEvent(int bytes){
  while (Wire.available()){
    data = Wire.read();
    Serial.print("data received: ");
    Serial.println(data);
  }
}

void sendData(){
  byte idata[24];
  Serial.print("sendData: ");
  memcpy(idata,raw.b,sizeof(raw.b));
  memcpy(idata+sizeof(raw.b),dcShift.b,sizeof(dcShift.b));
  memcpy(idata+sizeof(raw.b)+sizeof(dcShift.b),out.b,sizeof(out.b));
  memcpy(idata+sizeof(raw.b)+sizeof(dcShift.b)+sizeof(out.b),raw2.b,sizeof(raw2.b));
  memcpy(idata+sizeof(raw.b)+sizeof(dcShift.b)+sizeof(out.b)+sizeof(raw2.b),dcShift2.b,sizeof(dcShift2.b));
  memcpy(idata+sizeof(raw.b)+sizeof(dcShift.b)+sizeof(out.b)+sizeof(raw2.b)+sizeof(dcShift2.b),out2.b,sizeof(out2.b));
  Serial.println(Wire.write(idata,24));
}

void loop() {
  // put your main code here, to run repeatedly:
}
