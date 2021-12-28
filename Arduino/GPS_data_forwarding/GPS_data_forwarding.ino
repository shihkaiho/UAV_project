#include <SoftwareSerial.h>

SoftwareSerial mySerial(4, 3); // RX, TX

void setup()
{
  Serial.begin(9600);
  while (!Serial) {}
  mySerial.begin(9600);
}

void loop() // run over and over
{
  if (mySerial.available())
    Serial.write(mySerial.read());
}
