int pwm = 255;
int dir = 0;
int enc = 0;
int cnt = 0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  digitalWrite(12, dir);
  analogWrite(6, pwm);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (millis() % 10 == 0) {
    enc = analogRead(A0);
    if (enc > 1000) {
      cnt++;
    }

    if (dir == 0 && cnt > 200) {
      dir = 1;
      digitalWrite(12, dir);
      cnt = 0;
    }

    if (dir == 1 && cnt > 200) {
      dir = 0;
      digitalWrite(12, dir);
      cnt = 0;
    }
    Serial.println(cnt);
  }

}
