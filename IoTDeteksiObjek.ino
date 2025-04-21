#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <ESP32Servo.h>

const char* ssid = "POCO X3 Pro";
const char* password = "12345678";

Servo servo;  // Objek servo menggunakan ESP32Servo
int servoPin = 23; // Pin servo
int buzzerPin = 13; // Pin buzzer

AsyncWebServer server(80);

unsigned long servoStartTime = 0;
unsigned long buzzerStartTime = 0;
bool servoActive = false;
bool buzzerActive = false;

void setup() {
  Serial.begin(115200);

  // Setup WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());

  // Setup servo dan buzzer
  servo.attach(servoPin);
  servo.write(0); // Posisi awal servo di 90 derajat (netral)
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(buzzerPin, LOW);

  // Route untuk mengontrol servo
  server.on("/control_servo", HTTP_POST, [](AsyncWebServerRequest *request) {
    Serial.println("Pisang busuk terdeteksi - Servo bergerak");
    servo.write(90);          // Gerakkan servo ke posisi 180 derajat
    servoStartTime = millis(); // Catat waktu mulai servo aktif
    servoActive = true;       // Aktifkan flag servo
    request->send(200, "text/plain", "Servo state changed");
  });

  // Route untuk mengontrol buzzer
  server.on("/control_buzzer", HTTP_POST, [](AsyncWebServerRequest *request) {
    Serial.println("Pisang matang terdeteksi - Buzzer menyala");
    digitalWrite(buzzerPin, HIGH); // Nyalakan buzzer
    buzzerStartTime = millis();    // Catat waktu mulai buzzer aktif
    buzzerActive = true;           // Aktifkan flag buzzer
    request->send(200, "text/plain", "Buzzer state changed");
  });

  server.begin();
}

void loop() {
  // Cek apakah servo aktif dan waktu sudah lebih dari 1 detik
  if (servoActive && (millis() - servoStartTime >= 1000)) {
    servo.write(0);         // Kembalikan servo ke posisi netral
    servoActive = false;     // Nonaktifkan flag servo
    Serial.println("Servo kembali ke posisi netral");
  }

  // Cek apakah buzzer aktif dan waktu sudah lebih dari 1 detik
  if (buzzerActive && (millis() - buzzerStartTime >= 1000)) {
    digitalWrite(buzzerPin, LOW); // Matikan buzzer
    buzzerActive = false;         // Nonaktifkan flag buzzer
    Serial.println("Buzzer mati");
  }
}