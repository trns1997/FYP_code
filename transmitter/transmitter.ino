int adc1;
int adc2;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

}

void loop() {
  // put your main code here, to run repeatedly:
  adc1 = analogRead(A0) - 305;
  adc2 = analogRead(A1);
  Serial.print(adc1);
  Serial.print(",");
  Serial.println(adc2);
  delay(1);

}
