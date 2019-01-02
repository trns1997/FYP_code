void setup() {
  // put your setup code here, to run once:
  pinMode(11,OUTPUT);
  Serial.begin(115200);
}
int input = 0;
int out = 0;
void loop() {
  // put your main code here, to run repeatedly:
  input = analogRead(A1);
  out = map(input,0,1024,0,255);
  analogWrite(11,out);
  //delay(100);
//  Serial.println(out);
}
