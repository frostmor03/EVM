void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(D0, OUTPUT);
  pinMode(D1, INPUT)
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(D0, !digitalRead(D1))                      // wait for a second
}
