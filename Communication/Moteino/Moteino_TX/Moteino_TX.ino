// rf95_reliable_datagram_server.pde
// -*- mode: C++ -*-
// Example sketch showing how to create a simple addressed, reliable messaging server
// with the RHReliableDatagram class, using the RH_RF95 driver to control a RF95 radio.
// It is designed to work with the other example rf95_reliable_datagram_client
// Tested with Anarduino MiniWirelessLoRa, Rocket Scream Mini Ultra Pro with the RFM95W 

#include <RHReliableDatagram.h>
#include <RH_RF95.h>
#include <SPI.h>
#include "LowPower.h"

#define CLIENT_ADDRESS 1
#define SERVER_ADDRESS 2

const int pin = 0;
unsigned int count = 0;
//unsigned long timing = millis();
//int32_t timeout = 10000;

void wakeUp()
{
  
}

union An
{
  int n;
  uint8_t b[2];
}an;

union Temp
{
  float n;
  uint8_t b[4];
}temp;

union Hum
{
  uint32_t n;
  uint8_t b[4];
}hum;

// Singleton instance of the radio driver
RH_RF95 driver;
//RH_RF95 driver(5, 2); // Rocket Scream Mini Ultra Pro with the RFM95W

// Class to manage message delivery and receipt, using the driver declared above
RHReliableDatagram manager(driver, SERVER_ADDRESS);

// Need this on Arduino Zero with SerialUSB port (eg RocketScream Mini Ultra Pro)
//#define Serial SerialUSB

An an1;
Temp temp1;
Hum hum1;

void setup() 
{
  // Rocket Scream Mini Ultra Pro with the RFM95W only:
  // Ensure serial flash is not interfering with radio communication on SPI bus
//  pinMode(4, OUTPUT);
//  digitalWrite(4, HIGH);

  //Serial.begin(9600);
 // while (!Serial) ; // Wait for serial port to be available
  if (!manager.init())
    Serial.println("init failed");
  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then 
  // you can set transmitter powers from 5 to 23 dBm:
  //driver.setTxPower(23, false);
  // If you are using Modtronix inAir4 or inAir9,or any other module which uses the
  // transmitter RFO pins and not the PA_BOOST pins
  // then you can configure the power transmitter power for -1 to 14 dBm and with useRFO true. 
  // Failure to do that will result in extremely low transmit powers.
//  driver.setTxPower(14, true);
  // You can optionally require this module to wait until Channel Activity
  // Detection shows no activity on the channel before transmitting by setting
  // the CAD timeout to non-zero:
//  driver.setCADTimeout(10000);
  count = 0;
  driver.setFrequency(380);
  pinMode(pin, INPUT);  
}

uint8_t data[] = { //an1.b[0], an1.b[1], 
                 //temp1.b[0], temp1.b[1], temp1.b[2], temp1.b[3]};//,
                // hum1.n, hum1.b[0], hum1.b[1], hum1.b[2], hum1.b[3]};
                "Things and Stuff"};
// Dont put this on the stack:
uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];

void loop()
{
  // Allow wake up pin to trigger interrupt on low.
//  attachInterrupt(0, wakeUp, LOW);
    
  //if (manager.available())
  //{
    
    //Serial.println(an1.n);
    temp1.n = 82.34;
    uint8_t data[] = {// an1.b[0], an1.b[1], 
                     //temp1.b[0], temp1.b[1], temp1.b[2], temp1.b[3]};//,
                  // hum1.n, hum1.b[0], hum1.b[1], hum1.b[2], hum1.b[3]};
                      an1.b[0],an1.b[1]};
    // Wait for a message addressed to us from the client
    uint8_t len = sizeof(buf);
    uint8_t from;
    if (manager.recvfromAck(buf, &len, &from))
    {
      Serial.print("got request from : 0x");
      Serial.print(from, HEX);
      Serial.print(": ");
      Serial.println((char*)buf);
      an1.n = count++;
      // Send a reply back to the originator client
      if (!manager.sendtoWait(data, sizeof(data), from))
        Serial.println("sendtoWait failed");
    }
   /* if((timeout - timing) <= 0)
    {
       // Enter power down state with ADC and BOD module disabled.
       // Wake up when wake up pin is low.
       Serial.println("Sleeping");
       manager.sendtoWait(data, sizeof(data), from);
       timing = millis();
       LowPower.powerDown(SLEEP_FOREVER, ADC_OFF, BOD_OFF); 
    }*/
  //}
    // Disable external pin interrupt on wake up pin.
   // detachInterrupt(0); 
}
