unsigned long timer = 0;
int pin[2] = {A1, A2};
const int bufSize = 60;
int inputs[bufSize] = {0};
int inputs2[bufSize]= {0};
int pointer, i = 0;
unsigned long sum,sum2 = 0;

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
  pinMode(11, OUTPUT);
  timer = millis();
}

void loop() {
  // put your main code here, to run repeatedly:
  if ( (micros() - timer) > 30) {
    //Serial.println(micros()-timer);
    inputs[pointer] = analogRead(pin[0]);
    inputs2[pointer]= analogRead(pin[1]);
    raw.val = inputs[pointer];
    raw2.val = inputs2[pointer];
    
    Serial.write(raw.b,4);
    Serial.write(dcShift.b,4);
    Serial.write(out.b,4);
    Serial.write(raw2.b,4);
    Serial.write(dcShift2.b,4);
    Serial.write(out2.b,4);
    //Serial.println(inputs[pointer]);
    
    if (pointer == bufSize - 1) {
      dcShift.val = 0;
      dcShift2.val = 0;
      for (i = 0; i < bufSize; i++) {
        dcShift.val += inputs[i];
        dcShift2.val += inputs2[i];;
      }
      dcShift.val /= bufSize;
      dcShift2.val /= bufSize;
      //Serial.println(dcShift.val);
      sum = 0;
      sum2= 0;
      for (i = 0; i < bufSize; i++) {
        inputs[i] = inputs[i] - dcShift.val;
        sum += pow(inputs[i], 2);
        inputs2[i] = inputs2[i] - dcShift2.val;
        sum2 += pow(inputs2[i], 2);
      }
      out.val = sqrt(sum / bufSize);
      out2.val = sqrt(sum2 / bufSize);
      //Serial.println(out.val);
      pointer = -1;
    }
    pointer++;
    timer = micros();
  }
}
