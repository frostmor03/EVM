#include <Servo.h>

Servo servo;  // Создаем объект Servo

int potPin = A0;  // Пин, к которому подключен потенциометр
int angle = 0;   // Угол поворота сервопривода

void setup() {
  servo.attach(D0, 500, 2500);  // Подключаем сервопривод к пину D0
}

void loop() {
  // Считываем значение с потенциометра
  int potValue = analogRead(potPin);
  
  // Преобразуем значение потенциометра (0-4095) в угол поворота сервопривода (0-180)
  angle = map(potValue, 0, 4095, 0, 180);
  
  // Поворачиваем сервопривод на заданный угол
  servo.write(angle);
  
  delay(15);  // Небольшая задержка для стабилизации
}