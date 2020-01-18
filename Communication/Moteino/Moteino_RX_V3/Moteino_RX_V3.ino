// rf95_reliable_datagram_server.pde
// -*- mode: C++ -*-
// Example sketch showing how to create a simple addressed, reliable messaging server
// with the RHReliableDatagram class, using the RH_RF95 driver to control a RF95 radio.
// It is designed to work with the other example rf95_reliable_datagram_client
// Tested with Anarduino MiniWirelessLoRa, Rocket Scream Mini Ultra Pro with the RFM95W 

#include <RHReliableDatagram.h>
#include <RH_RF95.h>
#include <SPI.h>
#include <Wire.h>

//#include "rand.h"
#include "Seeed_BME280.h"

#define CLIENT_ADDRESS 1
#define SERVER_ADDRESS 2

const int pin = 2;
const int d1 = 3;
const int d2 = 4;

//unsigned long timing = millis();
//int32_t timeout = 10000;
int count = 0;
int firstTime = 1;

void wakeUp()
{
  Serial.println("Waiting");
}


union //temperature
{
  float n;
  uint8_t b[4];
}temp;

union //humidity
{
  uint32_t n;
  uint8_t b[4];
}hum;

union //rain gaige
{
  int n;
  uint8_t b[2];
}rain;

union //wind speed
{
  int n;
  uint8_t b[2];
}spe;

union //wind direction
{
  int n;
  uint8_t b[2];
}wind;

union //precipitation
{
  int n;
  uint8_t b[2];
}pre;

union //Battery voltage
{
  int n;
  uint8_t b[2];
}v;

union //photoresistor
{
  int n;
  uint8_t b[2];
}r;

// Singleton instance of the radio driver
RH_RF95 driver;
//RH_RF95 driver(5, 2); // Rocket Scream Mini Ultra Pro with the RFM95W

//Temperature Driver instance
BME280 bme280;

// Class to manage message delivery and receipt, using the driver declared above
RHReliableDatagram manager(driver, SERVER_ADDRESS);

// Need this on Arduino Zero with SerialUSB port (eg RocketScream Mini Ultra Pro)
//#define Serial SerialUSB

//Rain rain1;
//Temp temp1;
//Hum hum1;
//Res res1;
//Spe spe1;
//Wind wind1;
//Pre pre1;
//V v1;
//R r1;

void setup() 
{
  // Rocket Scream Mini Ultra Pro with the RFM95W only:
  // Ensure serial flash is not interfering with radio communication on SPI bus
 // pinMode(4, INPUT);
//  digitalWrite(4, HIGH);
  Serial.begin(9600);
  //while (!Serial) ; // Wait for serial port to be available
  if (!manager.init())
    Serial.println("init failed");
  if(!bme280.init())
    Serial.println("Device error!");
    
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
  driver.setFrequency(380);
  pinMode(pin, OUTPUT);
  pinMode(d1, INPUT); // Rain gaige
  pinMode(d2, INPUT); // windspeed
  pinMode(A0,INPUT); // wind direction
  pinMode(A1, INPUT); // battery voltage
  pinMode(A2, INPUT); // photo resistor
  pinMode(A3, INPUT); // precipitation (snow detector)
  pinMode(A4, INPUT); // sca bme    I2C
  pinMode(A5, INPUT); // scl bme    I2C
}

uint8_t data[] = { rain.b[0], rain.b[1], 
                 temp.b[0], temp.b[1], temp.b[2], temp.b[3],
                 hum.b[0], hum.b[1], hum.b[2], hum.b[3],
                 spe.b[0], spe.b[1], wind.b[0],
                 wind.b[1], pre.b[0], pre.b[1], v.b[0], v.b[1],
                 r.b[0], r.b[1]};
// Dont put this on the stack:
uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];

void loop()
{
  // Serial.println("Working");
  // Allow wake up pin to trigger interrupt on low.
 // attachInterrupt(0, wakeUp, RISING);
  //LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);
  //LowPower.powerDown(SLEEP_FOREVER, ADC_OFF, BOD_OFF);
 // LowPower.idle(SLEEP_8S, ADC_OFF, TIMER2_OFF, TIMER1_OFF, TIMER0_OFF, 
    //            SPI_OFF, USART0_OFF, TWI_OFF);
 // detachInterrupt(0); 
  //if (manager.available())
  //{
    
    rain.n = digitalRead(d1);
    spe.n = digitalRead(d2);
    wind.n = analogRead(A0);
    pre.n = analogRead(A3);
    v.n = 10* analogRead(A1);
    r.n = analogRead(A2);
    temp.n = bme280.getTemperature();
    hum.n=  bme280.getHumidity();
    Serial.println(temp.n);
    Serial.println(hum.n);
    count = 1;
    firstTime = 0;
    //test code//    
    //temp.n = 82.34;
    //hum.n = 76;
    rain.n = 32;
    //spe.n = 3;
    //wind.n = 4;
    //pre.n = 5;
    //v.n = 6;
    //r.n = 7;
    //----------------//
    uint8_t data[] = { rain.b[0], rain.b[1], 
                      temp.b[0], temp.b[1], temp.b[2], temp.b[3],
                      hum.b[0], hum.b[1], hum.b[2], hum.b[3]};//,
                      //spe.b[0], spe.b[1], wind.b[0],
                      //wind.b[1], pre.b[0], pre.b[1], v.b[0], v.b[1],
                      //r.b[0], r.b[1]};
   // Serial.println(count);
    // Wait for a message addressed to us from the client
    uint8_t len = sizeof(buf);
    uint8_t from;
    if (manager.recvfromAck(buf, &len, &from))
    {
     // Serial.print("got request from : 0x");
     // Serial.print(from, HEX);
     // Serial.print(": ");
     // Serial.println((char*)buf);
      
      // Send a reply back to the originator client
      if (!manager.sendtoWait(data, sizeof(data), from))
        Serial.println("sendtoWait failed");
    }

 

    
  //}

  //delay(100);
   
}
