#include <ELECHOUSE_CC1101.h>
#include "packets.h"
//#include <time.h>

// These examples are from the Electronics Cookbook by Simon Monk
// Connections (for an Arduino Uno)
// Arduino          CC1101
// GND              GND
// 3.3V             VCC
// 10               CSN/SS   **** Must be level shifted to 3.3V
// 11               SI/MOSI  **** Must be level shifted to 3.3V
// 12               SO/MISO
// 13               SCK      **** Must be level shifted to 3.3V
// 2                GD0

const int n = 61;
unsigned short int sequence = 0;
byte buffer[n] = "";

void setup() {
  Serial.begin(9600);
  Serial.println("Set line ending to New Line in Serial Monitor.");
  Serial.println("Enter Message");
  ELECHOUSE_cc1101.Init(F_433); // set frequency - F_433, F_868, F_965 MHz
}
Packet pckt, receive;
int len;
void loop() {
  if (Serial.available()) {
    pckt.data = Serial.readBytesUntil('\n', buffer, n);
    pckt.seqNum = sequence;
    buffer[pckt.data] = '\0';
    buffer[n-1] = pckt.seqNum;
    Serial.println((char *)buffer);
    ELECHOUSE_cc1101.SendData(buffer, pckt.data + pckt.seqNum);
   
    while( pckt.seqNum <= sequence){
      ELECHOUSE_cc1101.SendData(buffer, pckt.data + pckt.seqNum);
     // Serial.println(buffer[0]);
      len = ELECHOUSE_cc1101.ReceiveData(buffer);
     // Serial.println(len);
      buffer[len] = '\0';
      receive.data = buffer[0];
      sequence = buffer[n-1];
      Serial.print("Sequence:");
      Serial.println(buffer[n-1]);
      
    }
    Serial.println("Got ACK");
    
    
  }
}
