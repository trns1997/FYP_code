float count = 0;
float EMA_a = 0.02;     //initialization of EMA alpha
float EMA_S1 = 0;
float outputA = 0;
float outputB = 0;
float outputC = 0;
float freq = 0.3; //0.005-0.3
float input = 0;
float prev_input = 0;
int window = 20;
float inputs[20] = {};
int sinPWM[]={1,2,5,7,10,12,15,17,19,22,24,27,30,32,34,37,39,42,
44,47,49,52,54,57,59,61,64,66,69,71,73,76,78,80,83,85,88,90,92,94,97,99,
101,103,106,108,110,113,115,117,119,121,124,126,128,130,132,134,136,138,140,142,144,146,
148,150,152,154,156,158,160,162,164,166,168,169,171,173,175,177,178,180,182,184,185,187,188,190,192,193,
195,196,198,199,201,202,204,205,207,208,209,211,212,213,215,216,217,219,220,221,222,223,224,225,226,227,
228,229,230,231,232,233,234,235,236,237,237,238,239,240,240,241,242,242,243,243,244,244,245,245,246,246,
247,247,247,248,248,248,248,249,249,249,249,249,255,255,255,255,249,249,249,249,249,248,
248,248,248,247,247,247,246,246,245,245,244,244,243,243,242,242,241,240,240,239,238,237,237,236,235,234,
233,232,231,230,229,228,227,226,225,224,223,222,221,220,219,217,216,215,213,212,211,209,208,207,205,204,
202,201,199,198,196,195,193,192,190,188,187,185,184,182,180,178,177,175,173,171,169,168,166,164,162,160,
158,156,154,152,150,148,146,144,142,140,138,136,134,132,130,128,126,124,121,119,117,115,113,110,108,106,
103,101,99,97,94,92,90,88,85,83,80,78,76,73,71,69,66,64,61,59,57,54,52,49,47,44,42,39,37,34,32,30,
27,24,22,19,17,15,12,10,7,5,2,1};

void setup() {
  // put your setup code here, to run once:
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  TCCR2B = (TCCR2B & 0b11111000) | 0x01;
  //  TCCR0B = (TCCR0B & 0b11111000) | 0x01;
  TCCR1B = (TCCR1B & 0b11111000) | 0x01;
  Serial.begin(115200);
  Serial.print(sizeof(sinPWM)/sizeof(int));
  //    Serial.println(TCCR2B,BIN);
  //    Serial.println(TCCR0B,BIN);
  //    Serial.println(TCCR0A,BIN);
  //    Serial.println(TCCR1A,BIN);
  //    Serial.println(TCCR1B,BIN);
  //    Serial.println(TCCR2A,BIN);
}

void loop() {
  // put your main code here, to run repeatedly;
  if (millis() % 10 == 0) {
    //    inputs[int(count) % window] = analogRead(A3);
    //    for (int i = 0; i < window; i++) {
    //      input += inputs[i];
    //    }
    //    input = input / window;
    //
    float sen1 = analogRead(A3);
    input = (EMA_a * sen1) + ((1 - EMA_a) * input);
//    Serial.println(input);

  }


  if (millis() % 1 == 0) {

    //    outputA = (255 / 2) * sin(count * freq) + (255 / 2);
    //    outputB = (255 / 2) * sin((count * freq) - ((2 * 120 * PI) / 180)) + (255 / 2);
    //    outputC = (255 / 2) * sin((count * freq) - (120 * PI) / 180) + (255 / 2);

    if (input > 600) {
      freq = (0.0006974 * input) - 0.41344;
      //        freq = float(int(freq)/10*10);
      outputA = (255.0 / 2.0) * sin(count * freq) + (255.0 / 2.0);
      outputB = (255.0 / 2.0) * sin((count * freq) - ((2.0 * 120.0 * PI) / 180.0)) + (255.0 / 2.0);
      outputC = (255.0 / 2.0) * sin((count * freq) - (120.0 * PI) / 180.0) + (255.0 / 2.0);
    } else if (input < 424) {
      freq = 0.3 - (0.000695755 * input);
      //        freq = float(int(freq/10)*10);
      outputA = (255.0 / 2.0) * sin(count * freq) + (255.0 / 2.0);
      outputB = (255.0 / 2.0) * sin((count * freq) - ((120.0 * PI) / 180.0)) + (255.0 / 2.0);
      outputC = (255.0 / 2.0) * sin((count * freq) - (2.0 * 120.0 * PI) / 180.0) + (255.0 / 2.0);
    }
    //    Serial.print(outputA);
    //    Serial.print(",");
    //    Serial.print(outputB);
    //    Serial.print(",");
    //    Serial.println(outputC);
    analogWrite(9, outputA);
    analogWrite(10, outputB);
    analogWrite(11, outputC);

//    Serial.println(freq);

    count++;
  }
}
