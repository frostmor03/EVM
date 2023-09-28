const int ledPin = D0;   
const int potPin = A0;   
int potValue = 0;        

void setup() {
  pinMode(ledPin, OUTPUT);
}

void loop() {

  potValue = analogRead(potPin);


  int pwmValue = map(potValue, 0, 65535, 0, 1023);


  analogWrite(ledPin, pwmValue);

  delay(10);  
}