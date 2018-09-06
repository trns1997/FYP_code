#include <Filters.h>
int adc;
float filterFrequency = 0.8;
int out;
float EMA_b = 0.3;
FilterOnePole lowpassFilter( LOWPASS, filterFrequency );
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(11, OUTPUT);
}

int i = 0;
const int Isize = 10;
int inputs[Isize] = {};
long outRMS = 0;

void loop() {
  // put your main code here, to run repeatedly:
  adc = analogRead(A1) - 305;
//  out = (EMA_b * lowpassFilter.input(abs(adc))) + ((1 - EMA_b) * out);
////  Serial.print(out);
////  Serial.print(",");
//
//  inputs[i] = sq(lowpassFilter.input(adc));
//  outRMS = 0;
//  for (int j = 0; j < Isize; j++) {
//    outRMS += inputs[j];
//  }
//  outRMS = sqrt(outRMS / Isize);
//  i++;
//  if (i > Isize) {
//    i = 0;
//  }
//
//  outRMS = ((outRMS * 3) > 50) ? 49 : outRMS * 3;
//  analogWrite(11, map(outRMS, 0, 50, 127, 255));



  Serial.println(adc);
  delay(1);
}
