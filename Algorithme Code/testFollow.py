#Main file to run for detection with the complete system

from IntegratedDetection import *

if __name__ == '__main__':
    complete_model, power_detector, motor_arduino, TCPsocket, compass = init(datasets_directory = "datasets/Domain/", COM_Power = 'COM9', COM_Motor = 'COM7', COM_compass = 'COM10') #Initializing all components

    func = lambda azi, ele: getPower(azi, ele, power_detector, motor_arduino, TCPsocket, 'AntennaControl\Antenna_control_phase_steps_1deg_resolution.txt') #Function to get the power at particular position
    func(0,0) #Initialize system's position
    
    from CS import *
    
    x, f, k = opportunisticCS(lambda x: -1*func(x[0], x[1]), [0, -40], 0, float('inf'))