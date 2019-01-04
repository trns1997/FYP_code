unsigned long timer = 0;
int pin[2] = {A1, A2};
const int bufSize = 60;
int inputs[bufSize] = {0};
int inputs2[bufSize] = {0};
int pointer, i = 0;
int EMA_1 = 0;
int EMA_2 = 0;
unsigned long sum, sum2 = 0;

#include <Wire.h>
#define SLAVE_ADDRESS 0x0A

union cvd {
  float val;
  byte b[4];
} out, out2, out3, out4;

union cvl {
  unsigned long val;
  byte b[4];
} dcShift, dcShift2;

union cvi {
  int val;
  byte b[4];
} raw, raw2;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  //  pinMode(11, OUTPUT);
  timer = millis();
  out3.val = 0;
  out4.val = 0;
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(sendData);
  delay(3000);
}

void receiveEvent(int bytes) {
  while (Wire.available()) {
    int data = Wire.read();
    //    Serial.print("data received: ");
    //    Serial.printl/n(data);
  }
}

void sendData() {
  byte idata[16];
  //  Serial.print("sendData: ");
  out3.val = 0;
  out4.val = 0;
  memcpy(idata, out.b, 4);
  memcpy(idata + 4, out2.b, 4);
  memcpy(idata + 8, out3.b, 4);
  memcpy(idata + 12, out4.b, 4);
  //memcpy(idata+16,dcShift2.b,4);
  //memcpy(idata+20,out2.b,4);
  //  Serial.println(Wire.write/(idata,16));
}

void loop() {
  // put your main code here, to run repeatedly:
  if ( (micros() - timer) > 5) {
    //Serial.println(micros()-timer);
    inputs[pointer] = analogRead(pin[0]);
    inputs2[pointer] = analogRead(pin[1]);
    raw.val = inputs[pointer];
    raw2.val = inputs2[pointer];
    //    Serial.println(inputs[pointe/r]);

    if (pointer == bufSize - 1) {
      long temp = 0;
      long temp2 = 0;
      for (i = 0; i < bufSize; i++) {
        temp += inputs[i];
        temp2 += inputs2[i];;
      }
      dcShift.val = temp / bufSize;
      dcShift2.val = temp2 / bufSize;
      //Serial.println(dcShift.val);
      sum = 0;
      sum2 = 0;
      for (i = 0; i < bufSize; i++) {
        inputs[i] = inputs[i] - dcShift.val;
        sum += pow(inputs[i], 2);
        inputs2[i] = inputs2[i] - dcShift2.val;
        sum2 += pow(inputs2[i], 2);
      }
      EMA_1 = sqrt(sum / bufSize);
      EMA_2 = sqrt(sum2 / bufSize);
      out.val = (0.3*EMA_1) + (0.7*out.val);
      out2.val = (0.3*EMA_2) + (0.7*out2.val);
      //Serial.println(out.val);
      pointer = -1;
      Serial.write(raw.b, 4);
      Serial.write(dcShift.b, 4);
      Serial.write(out.b, 4);
      Serial.write(raw2.b, 4);
      Serial.write(dcShift2.b, 4);
      Serial.write(out2.b, 4);
    }
    pointer++;
    timer = micros();
  }
}
