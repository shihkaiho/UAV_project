#include <SPI.h>
#include <LoRa.h>

String str;
int packetSize;
void setup() {
  Serial.begin(9600);
  if (!LoRa.begin(915E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
}

void loop() {
  if(Serial.available())
  {
    //read form serial
    str = Serial.readStringUntil('\n');
    //send to LoRa
    LoRa.beginPacket();
    LoRa.print(str);
    LoRa.endPacket();
  }
  packetSize = LoRa.parsePacket();
  if (packetSize) {
    //read from LoRa
    str = "";
    while (LoRa.available()) {
      str += (char)LoRa.read();
    }
    //send to serial
    Serial.println(str);
  }
  
}
