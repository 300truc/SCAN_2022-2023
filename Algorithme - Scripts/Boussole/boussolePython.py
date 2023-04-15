import serial
import time
import schedule

def main_func():
    arduino = serial.Serial('com#', 9600)
    print('Serial connection established with Arduino')
    arduino_data = arduino.readline()
    decoded_values = str(arduino_data[0:len(arduino_data)].decode("utf-8"))

    print(f'Heading from Arduino: {decoded_values}')

    arduino_data = 0
    arduino.close()
    print('Connection closed')


    # ------------------ Main -------------------

    schedule.every(10).seconds.do(main_func)

    while True:
        schedule.run_pending()
        time.sleep(1)
