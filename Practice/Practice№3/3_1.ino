#include <SPI.h>
#include <WiFi.h>

const char* ssid = "ASOIU";
const char* pass = "kaf.asoiu.48";
int status = WL_IDLE_STATUS;

int pingResult;

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    continue;
  }

  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi Shield не обнаружен");
    // Прекратить выполнение:
    while (true);
  }

  while (status != WL_CONNECTED) {
    Serial.print("Попытка подключения к сети WPA SSID: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);

    delay(5000);
  }

  Serial.println("Вы подключены к сети");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (Serial.available()) {
    String hostname = Serial.readStringUntil('\n');
    Serial.print("Пинг ");
    Serial.print(hostname);
    Serial.print(": ");

    IPAddress ip;
    if (WiFi.hostByName(hostname.c_str(), ip)) {
      pingResult = WiFi.ping(ip);

      if (pingResult >= 0) {
        Serial.print("Ураа! RTT = ");
        Serial.print(pingResult);
        Serial.println(" мс");
      } else {
        Serial.print("ОШИБКА! Код ошибки: ");
        Serial.println(pingResult);
      }
    } else {
      Serial.println("Не удалось разрешить имя хоста");
    }
    delay(5000);
  }
}
