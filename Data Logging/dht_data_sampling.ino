#include "dht.h"
#define dht_pin 2 // The Analog or Digital Pin that the sensor is connected to.
 
dht DHT;
 
void setup() {
 
  Serial.begin(9600);
  delay(1000); // Wait before accessing Sensor.
 
} // end "setup()"
 
void loop() {
  // Start of Program.
 
    DHT.read11(dht_pin);
    
    Serial.print(DHT.humidity);
    Serial.print(",");
    Serial.print(DHT.temperature);
    Serial.println();
    
    delay(5000); // Wait 5 seconds before accessing sensor again.
 
  // Fastest should be once every two seconds.
 
} // end loop() 