#Gradient detection for satellite following

import numpy as np
from IntegratedDetection import *

def simplex_gradient(func, x0, delta):
    n = len(x0)
    grad = np.zeros(n)
    f = func(x0)
    for i in range(n):
        step = np.zeros(n)
        step[i] = delta
        fi = func(x0 + step)
        grad[i] = (fi - f)/(delta)
    return grad

def gradient_optimizer(func, x0, tol, n, tau = 0.5):
    k = 0
    delta = 1
    while k <=n and delta > tol:
        d = -simplex_gradient(func, x0, delta)
        if np.linalg.norm(d) < tol:
            return x0
        k += 1
        fi = func(x0 + delta*d)
        if fi < func(x0):
            f = fi
            x0 += delta*d
            delta = np.min([delta/tau, 4])
        else:
            delta = np.max([delta*tau, 0.5])
            
    return x0

if __name__ == '__main__':
    import time
    from CS import *
    
    start_time = time.time()
    
    f = 28E9
    fs = '28.'
    
    complete_model, power_detector, motor_arduino, TCPsocket, compass = init(datasets_directory = "datasets/Domain/", COM_Power = 'COM5', COM_Motor = 'COM7', COM_compass = 'COM12', f = fs) #Initializing all components

    power = lambda azi, ele: getPower(azi, ele, power_detector, motor_arduino, TCPsocket, 'AntennaControl\Antenna_control_phase_steps_1deg_resolution.txt', f = f) #Function to get the power at particular position
    power(0,0) #Initialize system's position
    
    x0 = opportunisticCS(lambda x0: -1*power(x0[0], x0[1]), x0 = [0, -30], tol = 0, neval = float('inf'))
    #x0 = gradient_optimizer(lambda x0: -1*power(x0[0], x0[1]), x0 = [0, -30], tol = 0, n = float('inf')) #Find the position of the system

    #Print the source's position
    print("Best azimuth = "+str(x0[0])+"\t Best elevation = "+str(x0[1]))
    