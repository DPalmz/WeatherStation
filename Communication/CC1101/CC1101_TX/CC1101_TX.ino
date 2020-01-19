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
unsigned short int sequence = 0;
byte buffer[n] = "";


void setup() {
  Serial.begin(9600);
  Serial.println("Set line ending to New Line in Serial Monitor.");
  Serial.println("Enter Message");
  ELECHOUSE_cc1101.Init(F_433); // set frequency - F_433, F_868, F_965 MHz
  // initialize timer1 

  noInterrupts();           // disable all interrupts

  TCCR1A = 0;

  TCCR1B = 0;

  TCNT1 = 0;

  
  OCR1A = 0xFFFF; // Max value for overflow for now

 // TCCR1B |= (1 << WGM12);   // CTC mode

  TCCR1B |= (1 << CS12);    // 256 prescaler 

  

  interrupts();             // enable all interrupts

}
Packet pckt, recieve;

ISR(TIMER1_OVR_vect){          // timer compare interrupt service routine
    //Resend packet
    ELECHOUSE_cc1101.SendData(buffer, pckt.data + pckt.seqNum);
    int len = ELECHOUSE_cc1101.ReceiveData(buffer);
    buffer[len] = '\0';
    recieve.seqNum = buffer[n];
    Serial.println("Interrupt");
    //TOV1 = 0; //Reset flag
    
}


void loop() {
  if (Serial.available()) {
    pckt.data = Serial.readBytesUntil('\n', buffer, n);
    pckt.seqNum = sequence;
    buffer[pckt.data] = '\0';
    buffer[n-1] = pckt.seqNum;
    Serial.println((char *)buffer);
    
    ELECHOUSE_cc1101.SendData(buffer, pckt.data + pckt.seqNum);
    TCNT1 = 0; // clear timer
    TIMSK1 |= (1 << TOIE0);  // enable timer compare interrupt
    //call_timer(0, 180);
    int len = ELECHOUSE_cc1101.ReceiveData(buffer);
    while (recieve.seqNum <= sequence) {

    }
    TIMSK1 &= ~(1 << TOIE0); // turn off the timer interrupt

  }
}
