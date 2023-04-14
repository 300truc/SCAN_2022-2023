#Main file to run for detection with the complete system

from IntegratedDetection import *

if __name__ == '__main__':
    import time
    from CS import *
    
    start_time = time.time()
    
    f = 28E9
    fs = '28.'
    
    complete_model, power_detector, motor_arduino, TCPsocket, compass = init(datasets_directory = "datasets/Domain/", COM_Power = 'COM5', COM_Motor = 'COM7', COM_compass = 'COM12', f = fs) #Initializing all components

    func = lambda azi, ele: getPower(azi, ele, power_detector, motor_arduino, TCPsocket, 'AntennaControl\Antenna_control_phase_steps_1deg_resolution.txt', f = f) #Function to get the power at particular position
    func(0,0) #Initialize system's position
    best_azi, best_ele, data = detect(func, [-180, -30], [180, 30], [9, 3], complete_model, tol = 10**-3) #Find the position of the system

    #Print the source's position
    print("Best azimuth = "+str(best_azi)+"\t Best elevation = "+str(best_ele))
    
    print("Time = "+str(time.time() - start_time))
    
    x0 = opportunisticCS(lambda x0: -1*func(x0[0], x0[1]), x0 = [best_azi, best_ele], tol = 0, neval = float('inf'))

    #Plot the detection pattern (optional)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter(data[:,0], data[:,2], data[:,3])
    ax.set_xlabel('A [°]')
    ax.set_ylabel('h [°]')
    plt.show()

    motorCommand(motor_arduino, 0)