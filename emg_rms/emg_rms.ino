#include <Filters.h>
int adc[2] = {0,0};
float filterFrequency = 0.8;
int out[2] = {0,0};
int pin[2] = {A1,A2};
float EMA_b = 0.3;
FilterOnePole lowpassFilter( LOWPASS, filterFrequency );
FilterOnePole lowpassFilter2( LOWPASS, filterFrequency );
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(11, OUTPUT);
}

int i = 0;
int k = 0;
const int Isize = 10;
int inputs[2][Isize] = {};
int outRMS[2] = {0,0};
int diff = 0;

void loop() {
  // put your main code here, to run repeatedly:
  for(k=0;k<2;k++){
    adc[k] = analogRead(pin[k]) - 305;
    if (k==0){
      out[k] = (EMA_b * lowpassFilter.input(abs(adc[k]))) + ((1 - EMA_b) * out[k]);
      inputs[k][i] = sq(lowpassFilter.input(adc[k]));
      }
      else{
      out[k] = (EMA_b * lowpassFilter2.input(abs(adc[k]))) + ((1 - EMA_b) * out[k]);
      inputs[k][i] = sq(lowpassFilter2.input(adc[k]));
      }
  //  Serial.print(out);
  //  Serial.print(",");
    outRMS[k] = 0;
    for (int j = 0; j < Isize; j++) {
      outRMS[k] += inputs[k][j];
    }
    outRMS[k] = sqrt(outRMS[k] / Isize);
    i++;
    if (i > Isize) {
      i = 0;
    }
  }
  diff = outRMS[0] - outRMS[1];
  //Serial.print(outRMS[0]);
  //Serial.print(",");
  //Serial.println(outRMS[1]);  
  //outRMS = ((outRMS * 3) > 50) ? 49 : outRMS * 3;
  analogWrite(11, map(diff, -25, 25, 0, 255));

  Serial.println(map(diff, -25, 25, 0, 255));
  delay(10);
}
