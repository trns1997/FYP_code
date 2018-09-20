unsigned long timer = 0;
int pin[2] = {A1, A2};
const int bufSize = 400;
int inputs[bufSize] = {0};
int pointer, i = 0;
unsigned long avg, sum = 0;
double ans = 0;
const double EMA_b = 0.4;
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
    Serial.println(inputs[pointer]);
    if (pointer == bufSize - 1) {
      sum = 0;
      for (i = 0; i < bufSize; i++) {
        avg += inputs[i];
      }
      avg /= bufSize;
      //Serial.println(avg);
      for (i = 0; i < bufSize; i++) {
        inputs[i] = inputs[i] - avg;
        sum += pow(inputs[i], 2);
      }
      ans = sqrt(sum / bufSize);
      Serial.println(ans);
      //out = (EMA_b * ans + ((1 - EMA_b) * out));
      pointer = -1;
    }

    pointer++;
    timer = micros();
  }
}
