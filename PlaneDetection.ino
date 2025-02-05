//ip address: 192.168.4.1
#include <WiFiS3.h>
#include <WiFiServer.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <QMC5883LCompass.h>
#include <TinyGPS++.h>

//Declare WiFi Stuff
const char* ssid = "Arduino_AP";
const char* password = "helloworld";

WiFiServer server(23);

// Create objects for MPU6050, QMC5883L compass, and GPS
Adafruit_MPU6050 mpu;
QMC5883LCompass compass;
TinyGPSPlus gps;

// Variables for pitch, roll, and heading
float pitch, roll, heading;

void setup() {
  Serial.begin(9600);          // Start Serial Monitor communication
  Serial1.begin(9600);         // Use Serial1 for GPS module communication

  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }
  Serial.println("Starting Access Point...");
  
  if (!WiFi.beginAP(ssid, password)) {
    Serial.println("Failed to start Access Point!");
    while (true) {
      delay(1000); // Halt execution if Access Point setup fails
    }
  }

  // Print the IP address of the Access Point
  IPAddress IP = WiFi.softAPIP();
  Serial.print("Access Point IP Address: ");
  Serial.println(IP);

  // Start the server
  server.begin();
  Serial.println("Server started.");
  
  // Initialize MPU6050
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
  }

  // Set accelerometer and gyroscope ranges
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  // Initialize QMC5883L compass
  compass.init();
  compass.setCalibrationOffsets(-1305.00, -1406.00, -518.00);
  compass.setCalibrationScales(0.95, 0.88, 1.24);
  Serial.println("Initialization complete. Starting data acquisition...");
}

void loop() {
  WiFiClient client = server.available(); // Check for incoming clients
  if (client) {
    Serial.println("Client connected.");
    client.println("Welcome to the Arduino Telnet Server!\n");
    while (client.connected()) {
      // Process GPS data
      while (Serial1.available() > 0) {
        char c = Serial1.read();
        if (gps.encode(c)) {
            if (gps.location.isUpdated()) {
            // Print GPS location
            client.print("GPS Location: ");
            client.print("Latitude: ");
            client.print(gps.location.lat(), 6); // 6 decimal places for precision
            client.print(", Longitude: ");
            client.println(gps.location.lng(), 6);
            // Get MPU6050 sensor events
            sensors_event_t a, g, temp;
            mpu.getEvent(&a, &g, &temp);

            // Calculate pitch and roll
            pitch = atan2(a.acceleration.y, sqrt(a.acceleration.x * a.acceleration.x + a.acceleration.z * a.acceleration.z)) * 180.0 / PI;
            roll = atan2(-a.acceleration.x, a.acceleration.z) * 180.0 / PI;

            // Read compass heading
            compass.read();
            float x = compass.getX();
            float y = compass.getY();
            heading = atan2(y, x) * 180.0 / PI;
            if (heading < 0) heading += 360; // Normalize to 0–360 degrees

            // Print pitch, roll, and heading
            client.print("Pitch: ");
            client.print(pitch, 2);
            client.print("°, Roll: ");
            client.print(roll, 2);
            client.print("°, Heading: ");
            client.print(heading, 2);
            client.println("°");
            delay(100);
          }
        }
      }
    }
    client.stop();
    Serial.println("Client disconnected.");
  }
}