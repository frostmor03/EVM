void setup() {
  analogWriteFreq(10);
}

void loop() {
  int a = map(analogRead(A0), 0, 4095, 0, 180);
  analogWrite(D0, a);
  analogWrite(D1, a);
}