/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/AnalogReadSerial
*/
const int avgVal = 10;
float EMA_a = 0.02;     //initialization of EMA alpha
float EMA_S1 = 0;
float EMA_S2 = 0;
int on8[avgVal];
int on9[avgVal];
float mid = 255 / 2;
float grad = 1;
float out = mid;
int dz = 30;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(115200);
  pinMode(11, OUTPUT);   // sets the pin as output
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  float sensorValue1 = analogRead(A1);
  float sensorValue2 = analogRead(A2);
  EMA_S1 = (EMA_a * sensorValue1) + ((1 - EMA_a) * EMA_S1);
  EMA_S2 = (EMA_a * sensorValue2) + ((1 - EMA_a) * EMA_S2);
  Serial.print(EMA_S1);
  Serial.print(",");
  Serial.println(EMA_S2);
  //  Serial.print(",");
  //  Serial.println(EMA_S1 - EMA_S2);
  //  input = ((((EMA_S1-200)/1007)*487))/2;
  //  Serial.println(input);
  //  analogWrite(A3, input);
  //  if (EMA_S1 > dz) {
  //    out = grad * (EMA_S1 - dz) + mid;
  //  }
  //  else if (EMA_S1 < -dz) {
  //    out = grad * (EMA_S1 + dz) + mid;
  //  }
  //
  //  else {
  //    out = mid;
  //  }
  analogWrite(11, 127);
  //  Serial.println(out);
  delay(1);        // delay in between reads for stability
}
