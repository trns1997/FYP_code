float sinPWM[360] = {};

float outputA, outputB, outputC = 0;
int timer = 20; //1-20
unsigned int ptr = 0;
float spd = 0;
int dir = 1; // -1 anti-Clk, 0 stationary, 1 Clk

void setup() {
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  //Serial.begin(115200);
  for (int j = 0; j < 360; j++) {
    sinPWM[j] = (255.0 / 2.0) * sin((float(j) * PI) / 180.0) + (255.0 / 2.0);
  }
}

void loop() {

  if (millis() % 20 == 0) {
    timer = map(abs(spd - 512), 0, 512, 20, 2);
  }

  if (millis() % timer == 0) {
    outputA = sinPWM[ptr % 360];
    outputB = sinPWM[(ptr + 120) % 360];
    outputC = sinPWM[(ptr + 240) % 360];
    switch (dir){
      case -1:
        ptr--;
        break;
      case 0:
        outputA = 0;
        outputB = 0;
        outputC = 0;
        break;
      case 1:
        ptr++;
        break;
    }
    analogWrite(9, outputA);
    analogWrite(10, outputB);
    analogWrite(11, outputC);
  }
}
