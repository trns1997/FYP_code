float sinPWM[360] = {};

float EMA_a = 0.06;
float EMA_b = 0.3;
float outputA = 0;
float outputB = 0;
float outputC = 0;
float input = 0;
int input_filt = 0;
int timer = 20; //1-20
int i = 0;
int movement = 0; //0 lock, 1 clockwise, 2 anti-clckwise

void setup() {
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  TCCR2B = (TCCR2B & 0b11111000) | 0x01;
  TCCR1B = (TCCR1B & 0b11111000) | 0x01;
  Serial.begin(115200);

  for (int j = 0; j < 360; j++) {
    sinPWM[j] = (255.0 / 2.0) * sin((float(j) * PI) / 180.0) + (255.0 / 2.0);
    //    Serial.println(sinPWM[j]);
  }
  //  for (int k = 1; k < 360; k++) {
  //    sinPWM[k] = (EMA_a * sinPWM[k]) + ((1 - EMA_a) * sinPWM[k - 1]);
  //    Serial.println(sinPWM[k]);
  //  }
}

void loop() {

  if (millis() % 20 == 0) {
    input = analogRead(A3);
    input_filt = (EMA_a * input) + ((1 - EMA_a) * input_filt);

    if (input < 512) {
      movement = 1;
    } else {
      movement = 2;
    }
    if ((input > 412) and (input < 620)) {
      movement = 0;
    }
    timer = map(abs(input_filt - 512), 0, 512, 20, 2);
//    Serial.println(timer);
    //Serial.print(",");
    //    Serial.println(input_filt);
  }

  if (millis() % timer == 0) {
    outputA = (EMA_b * sinPWM[(i) % 360]) + ((1 - EMA_b) * outputA);
    outputB = (EMA_b * sinPWM[(i + 120) % 360]) + ((1 - EMA_b) * outputB);
    outputC = (EMA_b * sinPWM[(i + 240) % 360]) + ((1 - EMA_b) * outputC);
    //    Serial.print(outputA);
    //    Serial.print(",");
    //    Serial.print(outputB);
    //    Serial.print(",");
    //    Serial.println(outputC);
    if (movement > 0) {
      if (movement == 1) {
        i++;
      } else {
        i--;
      }
    }
//    analogWrite(9, 255);
//    analogWrite(10, 0);
//    analogWrite(11, 0);
      analogWrite(9, outputA);
      analogWrite(10, outputB);
      analogWrite(11, outputC);
    //    i++;
    if (i >= 360) {
      i = 0;
    }
    if (i < 0) {
      i = 359;
    }
  }
  //  if (millis() % timer == 0) {
  //    outputA = sinPWM[i];
  //    outputB = sinPWM[(i + 104) % 312];
  //    outputC = sinPWM[(i + 208) % 312];
  //    //    Serial.print(outputA);
  //    //    Serial.print(",");
  //    //    Serial.print(outputB);
  //    //    Serial.print(",");
  //    //    Serial.println(outputC);
  //    analogWrite(9, outputA);
  //    analogWrite(10, outputB);
  //    analogWrite(11, outputC);
  //    if (input > 600) {
  //      i++;
  //    } else if (input < 412) {
  //      i--;
  //    }
  //    if (i > 312) {
  //      i = 0;
  //    }
  //    if (i < 0) {
  //      i = 311;
  //    }
  //  }
  //
  //  //  if (millis() % 1 == 0) {
  //  //    if (input>600){
  //  //      ;
  //  //    }else if (input<412){
  //  //      ;
  //  //    }
  //  //  }

}


