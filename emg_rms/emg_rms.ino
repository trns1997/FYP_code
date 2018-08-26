#include <Filters.h>
int adc;
float filterFrequency = 0.8;
int out;
float EMA_b = 0.3;
FilterOnePole lowpassFilter( LOWPASS, filterFrequency );
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  adc = abs(analogRead(A1) - 305);
  out = (EMA_b * lowpassFilter.input(adc)) + ((1 - EMA_b) * out);
  Serial.println(out);
  delay(10);
}
