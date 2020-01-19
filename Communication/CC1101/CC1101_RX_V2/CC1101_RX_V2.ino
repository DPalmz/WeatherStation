#include <ELECHOUSE_CC1101.h>
#include "packets.h"

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


void setup()
{
  Serial.begin(9600);
  Serial.println("Rx");
  ELECHOUSE_cc1101.Init(F_433);  // set frequency - F_433, F_868, F_965 MHz
  ELECHOUSE_cc1101.SetReceive();
}

byte buffer[61] = {0};
unsigned short int sequence = 0;
Packet pckt;
int button = 2;

void loop()
{   /*if (pckt.data == 49){
      button = 1;
    }
    else if (pckt.data == 50){
      button = 2;
    }
    else if (pckt.data == 51){
      button = 3;
    }
    else if (pckt.data == 52){
      button = 4;
    }
    else{
      
    }*/
  if (ELECHOUSE_cc1101.CheckReceiveFlag())
  {
    Serial.println("Recieving");
    int len = ELECHOUSE_cc1101.ReceiveData(buffer);
    buffer[len] = '\0';
    if (buffer[n-1] > sequence){
       ELECHOUSE_cc1101.SendData(buffer, pckt.data + pckt.seqNum);
       Serial.println("Resend ACK");
    }
    pckt.data = button;
    pckt.seqNum = buffer[n-1];
    ++pckt.seqNum;
    sequence = pckt.seqNum;
    buffer[pckt.data] = '\0';
    buffer[n-1] = pckt.seqNum;
    ELECHOUSE_cc1101.SendData(buffer, pckt.data + pckt.seqNum);
    Serial.println(buffer[n-1]);
    Serial.println((char *) buffer);
    
  }
}
