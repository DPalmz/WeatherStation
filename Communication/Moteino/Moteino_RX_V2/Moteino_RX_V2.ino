// rf95_reliable_datagram_client.pde
// -*- mode: C++ -*-
// Example sketch showing how to create a simple addressed, reliable messaging client
// with the RHReliableDatagram class, using the RH_RF95 driver to control a RF95 radio.
// It is designed to work with the other example rf95_reliable_datagram_server
// Tested with Anarduino MiniWirelessLoRa, Rocket Scream Mini Ultra Pro with the RFM95W 

#include <RHReliableDatagram.h>
#include <RH_RF95.h>
#include <SPI.h>

#define CLIENT_ADDRESS 1
#define SERVER_ADDRESS 2

// Singleton instance of the radio driver
RH_RF95 driver;
//RH_RF95 driver(5, 2); // Rocket Scream Mini Ultra Pro with the RFM95W

// Class to manage message delivery and receipt, using the driver declared above
RHReliableDatagram manager(driver, CLIENT_ADDRESS);

// Need this on Arduino Zero with SerialUSB port (eg RocketScream Mini Ultra Pro)
//#define Serial SerialUSB

unsigned long starttime = millis();
int32_t resend, timeLeft;
bool state = 0;

union Temp //temperature
{
  float n;
  uint8_t b[4];
}temp;

union Hum //humidity
{
  uint32_t n;
  uint8_t b[4];
}hum;

union Rain //rain gaige
{
  int n;
  uint8_t b[2];
}rain;

union Spe //wind speed
{
  int n;
  uint8_t b[2];
}spe;

union Wind //wind direction
{
  int n;
  uint8_t b[2];
}wind;

union Pre //precipitation
{
  int n;
  uint8_t b[2];
}pre;

union V //Battery voltage
{
  int n;
  uint8_t b[2];
}v;

union R //photoresistor
{
  int n;
  uint8_t b[2];
}r;


Rain rain1;
Temp temp1;
Hum hum1;
Spe spe1;
Wind wind1;
Pre pre1;
V v1;
R r1;
int i = 0;
int blab;

void setup() 
{
  // Rocket Scream Mini Ultra Pro with the RFM95W only:
  // Ensure serial flash is not interfering with radio communication on SPI bus
//  pinMode(4, OUTPUT);
//  digitalWrite(4, HIGH);

  Serial.begin(9600);
  while (!Serial) ; // Wait for serial port to be available
  do{
      Serial.println("Moteino");
      blab = Serial.read();
  }while(blab != 0xFE);
  Serial.println("Good!");
  if (!manager.init())
    Serial.println("init failed");
  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then 
  // you can set transmitter powers from 5 to 23 dBm:
//  driver.setTxPower(23, false);
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
}

uint8_t data[] = "Hello World!";
// Dont put this on the stack:
uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];

void loop()
{
  //Serial.println("Sending to rf95_reliable_datagram_server");
  if (state == 0){  
    // Send a message to manager_server
    if (manager.sendtoWait(data, sizeof(data), SERVER_ADDRESS))
    {
      // Now wait for a reply from the server
      uint8_t len = sizeof(buf);
      uint8_t from;
      i = 0;
      rain1.b[0] = buf[i++];
      rain1.b[1] = buf[i++];  
      temp1.b[0] = buf[i++]; 
      temp1.b[1] = buf[i++];
      temp1.b[2] = buf[i++];
      temp1.b[3] = buf[i++];
      hum1.b[0] = buf[i++];
      hum1.b[1] = buf[i++];
      hum1.b[2] = buf[i++];
      hum1.b[3] = buf[i++];
      spe1.b[0] = buf[i++];
      spe1.b[1] = buf[i++];
      wind1.b[0] = buf[i++];
      wind1.b[1] = buf[i++];
      pre1.b[0] = buf[i++];
      pre1.b[1] = buf[i++];
      v1.b[0] = buf[i++];
      v1.b[1] = buf[i++];
      r1.b[0] = buf[i++];
      r1.b[1] = buf[i++];
      if (manager.recvfromAckTimeout(buf, &len, 2000, &from))
      {
       // Serial.println((int)an1.b[0]);
        Serial.println(rain1.n);
        Serial.println(temp1.n);
        Serial.println(hum1.n);
        Serial.println(spe1.n);
        Serial.println(wind1.n);
        Serial.println(pre1.n);
        Serial.println(v1.n);
        Serial.println(r1.n);
        //Serial.print("got request from : 0x");
       // Serial.print(from, HEX);
       // Serial.print(": ");
        //Serial.println((char*)buf);
      }
      else
      {
        Serial.println("No reply, is rf95_reliable_datagram_server running?");
      }
    }
    else
      //Serial.println("sendtoWait failed");
    
    resend = 300000; // 5 min in milliseconds
    if ((millis() - starttime) > resend){ //needed to use resend differently here
      state = 1;
      
    }
    delay(400);
  }
  else if (state == 1){
    resend = 10000;//3600000; // 1 hr in milliseconds
    starttime = millis();
    while ((timeLeft = resend - (millis() - starttime)) > 0){ 
      //Serial.println("Waiting loop");
    }
    state = 0;
  }
  
}
