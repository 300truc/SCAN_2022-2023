#Gradient detection for satellite following

import numpy as np
from IntegratedDetection import *

if __name__ == '__main__':
    import time
    from CS import *
    
    start_time = time.time()
    
    #Fréquence
    f = 28E9
    fs = '28.'
    
    complete_model, power_detector, motor_arduino, TCPsocket, compass = init(datasets_directory = "datasets/Domain/", COM_Power = 'COM5', COM_Motor = 'COM7', COM_compass = 'COM12', f = fs) #Initializing all components

    power = lambda azi, ele: getPower(azi, ele, power_detector, motor_arduino, TCPsocket, 'AntennaControl\Antenna_control_phase_steps_1deg_resolution.txt', f = f) #Function to get the power at particular position
    power(0,0) #Initialize system's position
    
    x0 = opportunisticCS(lambda x0: -1*power(x0[0], x0[1]), x0 = [0, -30], tol = 0, neval = float('inf'))

    #Print the source's position
    print("Best azimuth = "+str(x0[0])+"\t Best elevation = "+str(x0[1]))
    