//////// Project SCAN ////////
// Commande du moteur selon le mode pulse burst positioning
// Auteur : Kevin Shegani
// Dernière modification : 2023-04-07
//////////////////////////////

#include "math.h"

// Define Arduino pin numbers for the connection to the ClearPath controller cable.
// Wire colors refer to a standard Teknic ClearPath controller cable 
const int Enable = 6;  // ClearPath Enable Input;  +enable = BLU wire
const int Eneg = 12;   //                         -enable = ORN wire
const int InputA = 8;  // ClearPath Input A;       +InputA = WHT wire
const int Aneg = 10;   //                          -InputA = BRN wire
const int InputB = 9;  // ClearPath Input B;       +InputB = BLK wire
const int Bneg = 11;   //                          -InputB = YEL wire
const int HLFB = 4;    // ClearPath HLFB Output;   +HLFB   = GRN wire
const int Hneg = 5;    //                          -HLFB   = RED wire

int DwellTime = 1000; // Waiting time between each commanding moves
int cnt = 0;  // Motor increments
String angleRecv;
int angleRecvInt;

void setup() {
  //Define I/O pins
  Serial.begin(115200);
  pinMode(Enable, OUTPUT);
  pinMode(InputA, OUTPUT);
  pinMode(InputB, OUTPUT);
  pinMode(HLFB, INPUT_PULLUP);
  pinMode(Eneg, OUTPUT);
  pinMode(Aneg, OUTPUT);
  pinMode(Bneg, OUTPUT);
  pinMode(Hneg, OUTPUT);
  
  // Start off by ensuring that the motor is disabled before proceeding
  digitalWrite(Enable, LOW);
  delay(DwellTime);
 
  // Create ground pins for negative wires and put outputs to their initial states
  digitalWrite(Eneg, LOW);
  digitalWrite(Aneg, LOW);
  digitalWrite(Bneg, LOW);
  digitalWrite(Hneg, LOW);

  digitalWrite(InputA, LOW);
  digitalWrite(InputB, LOW);

  // Enabling motor to start command
  digitalWrite(Enable, HIGH);
  delay(DwellTime);
}


// Code stays in FetchIncrementCnts() indefinitly until an increment value is received 
// the increment is then sent to MoveCommand to command de rotation of the motor axis
void loop() {
  FetchIncrementCnts();
  MoveCommand(cnt);
}


//////////////////////////////////////////////////////////////////////////////////////////////////////////
//Implementation of fetchIncrementCnts function
/////////////////////////////////////////////////////////////////////////////////////////////////////////
void FetchIncrementCnts()
{
  /* fetchIncrement - captures the angle increment by using an arduino-python interface
   * to identify the value and direction of the next increment for the detection process
   * returns the increment cnt (int) to be used by the MoveCommand function
   */
   
   while(Serial.available()==0){}

   angleRecv = Serial.readStringUntil('\r');
   angleRecvInt = angleRecv.toInt(); 

   cnt = (int)((angleRecvInt*6400.0)/360.0);
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////
//Implementation of MoveCommand function
/////////////////////////////////////////////////////////////////////////////////////////////////////////
void MoveCommand(int incrementCnts)
{
  /*  MoveCommand - takes in the distance you would like to command, adjusts input A to accomodate the direction,
   *  and then pulses the Input B line a number of times equal to the magnitude of distance. AltSpeed is
   *  an optional TRUE/FALSE input that when true commands the motor to run at the alternate speed.
   *
   *  Commanded Motor : CPM-MCPV-2310S-ELN
   *  Native Resolution : 12800 cnts
   *  Commandable Resolution : 6400 cnts (ELN)
   */

  if(incrementCnts<0){
    digitalWrite(InputA,HIGH);  // CW rotation
  }
  else{
    digitalWrite(InputA,LOW);   // CCW rotation
  }

  for(int count=0;count<abs(incrementCnts);count++){
    digitalWrite(InputB, HIGH);
    digitalWrite(InputB, LOW);
  }
}