#include <Arduino.h>
#define led 5

uint8_t x;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(1);
  pinMode(led, OUTPUT);
}

void loop() {
  while (!Serial.available()); 
	x = Serial.readString().toInt(); 
	Serial.print(x + 1); 
}
 