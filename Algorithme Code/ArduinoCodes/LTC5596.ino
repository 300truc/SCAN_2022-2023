double slope = 0.0291; // slope in Volts per dB @28GHz
double xint = -37.1; //log intercept in dBm @28GHz
double solution = 0.0049; // LSB Size, refer to dn1050
double voltage = 0;
double power = 0;

int inputPin = A0;

void setup() {
  // put your setup code here, to run once:
  
  // initialize serial communication with computer:
  Serial.begin(9600);
  pinMode(7,OUTPUT);
  // initialize all the readings to 0:
  digitalWrite(7,HIGH);
}

void loop() {
  voltage = analogRead(inputPin) * solution;
  power = (voltage / slope) + xint;
  // send it to the computer as ASCII digits

  Serial.println(power);
  delay(30);        // delay in between reads for stability
}
