#include <MPU9250.h>

#include <Wire.h>

MPU9250 IMU (Wire, 0x68);
float fXm = 0;
float fYm = 0;
float fZm = 0;
float filteredX = 0;
float filteredY = 0;
float rollG = 0;
float pitchG = 0; 
float roll = 0;
float pitch = 0;
float dt;
unsigned long millisOld;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  IMU.begin();
  millisOld = millis();
}

void loop() {
  // put your main code here, to run repeatedly:
  IMU.readSensor();

  float AxCalibrated = 1.029449*(IMU.getAccelX_mss()-(0.166923))-0.004710*(IMU.getAccelY_mss()-(0.146021))+0.001555*(IMU.getAccelZ_mss()-(-2.999351));
  float AyCalibrated = -0.004710*(IMU.getAccelX_mss()-(0.166923))+1.015402*(IMU.getAccelY_mss()-(0.146021))-0.007142*(IMU.getAccelZ_mss()-(-2.999351));
  float AzCalibrated = 0.001555*(IMU.getAccelX_mss()-(0.166923))-0.007142*(IMU.getAccelY_mss()-(0.146021))+0.998811*(IMU.getAccelZ_mss()-(-2.999351));
  
//  float AxCalibrated = IMU.getAccelX_mss();
//  float AyCalibrated = IMU.getAccelY_mss();
//  float AzCalibrated = IMU.getAccelZ_mss();

  float MxCalibrated = 1.036100*(IMU.getMagX_uT()-(1.316616))-0.006614*(IMU.getMagY_uT()-(84.089027))-0.036995*(IMU.getMagZ_uT()-(33.742646));
  float MyCalibrated = -0.006614*(IMU.getMagX_uT()-(1.316616))+1.081616*(IMU.getMagY_uT()-(84.089027))+0.041503*(IMU.getMagZ_uT()-(33.742646));
  float MzCalibrated = -0.036995*(IMU.getMagX_uT()-(1.316616))+0.041503*(IMU.getMagY_uT()-(84.089027))+0.990367*(IMU.getMagZ_uT()-(33.742646));

  fXm = MxCalibrated;
  fYm = MyCalibrated;
  fZm = MzCalibrated;

//  float rollA  = atan2(fYa, sqrt(fXa*fXa + fZa*fZa));
//  float pitchA = atan2(fXa, sqrt(fYa*fYa + fZa*fZa));

  float rollA  = -atan2(AyCalibrated, sqrt(AxCalibrated*AxCalibrated + AzCalibrated*AzCalibrated));
  float pitchA = atan2(AxCalibrated, sqrt(AyCalibrated*AyCalibrated + AzCalibrated*AzCalibrated));

  float rollA_print = rollA*180.0/M_PI;
  float pitchA_print = pitchA*180.0/M_PI;

  dt = (millis()-millisOld)/1000.;
  millisOld = millis();

  rollG = rollG + (IMU.getGyroX_rads())*dt;
  pitchG = pitchG + (IMU.getGyroY_rads())*dt;

  float rollG_print = rollG*180.0/M_PI;;
  float pitchG_print = pitchG*180.0/M_PI;

  roll = (roll+((IMU.getGyroX_rads())*dt))*0.95+rollA*0.05;
  pitch = (pitch+((IMU.getGyroY_rads())*dt))*0.95+pitchA*0.05;

  float roll_print = roll*180.0/M_PI;;
  float pitch_print = pitch*180.0/M_PI;

  float fXm_comp = fXm*cos(pitch)+fYm*sin(roll)*sin(pitch)+fZm*cos(roll)*sin(pitch);
  // Tilt compensated Magnetic filed Y:
  float fYm_comp = fYm*cos(roll)-fZm*sin(roll);

  filteredX = filteredX*0.9+fXm_comp*0.1;
  filteredY = filteredY*0.9+fYm_comp*0.1;

  float Heading = (atan2(-filteredY,filteredX)*180.0)/M_PI;;


  //float Heading = (atan2(fYm_comp,fXm_comp)*180.0)/M_PI;
  if (Heading < 0) {
    Heading += 360;
  }
  
//  Serial.print(AxCalibrated);
//  Serial.print("\t");
//  Serial.print(AyCalibrated);
//  Serial.print("\t");
//  Serial.println(AzCalibrated);
//  Serial.print(roll_print);
//  Serial.print("\t");
//  Serial.println(pitch_print);
  Serial.println(Heading);
//  Serial.print("\t");
//  Serial.println(IMU.getGyroZ_rads());
  delay(100);
}
