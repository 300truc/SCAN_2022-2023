#Unit test to control the motor

import serial
arduinoData=serial.Serial('com7',115200)

while True:
    cmd=input('Envoie angle: ')
    cmd= cmd+'\r'
    arduinoData.write(cmd.encode())
