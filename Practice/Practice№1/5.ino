const int timerInterval = 1000;
struct repeating_timer timer;

void setup() {
  pinMode(D0, OUTPUT);
  pinMode(D1, OUTPUT);
  pinMode(D2, OUTPUT);

  add_repeating_timer_ms(timerInterval, timerISR, NULL, &timer); 
}

void loop() {

}

 volatile int n = 0;

bool timerISR(struct repeating_timer *timer) {
  digitalWrite(D0, LOW);
  digitalWrite(D1, LOW);
  digitalWrite(D2, LOW);
  n = (n + 1) % 3;
  digitalWrite(n, HIGH); 
  return true;
}
