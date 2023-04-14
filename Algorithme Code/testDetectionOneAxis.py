#Main file to run for detection with the complete system

from IntegratedDetection import *

#Integrate the motor, antenna and power detector together
def partialGetPower(azi, ele, power_detector, motor_arduino, antenna_socket, filename, RPM = 30):
    with open('currentpos.txt', 'r') as file:
        current_pos = float(file.readline())
        incr = azi - current_pos
    motorCommand(motor_arduino, azi)
    
    steer(ele, 'somme', antenna_socket, filename)
    power = readPower(power_detector, 15)
        
    #Printing the results for ease of debugging and information tracking
    print('Azimut = '+str(azi)+'\t Elevation = '+str(ele)+'\t Power = '+str(power))
    return power

def single_detect(func, modelfunc, tol = 10**-3):
    max_position = -30
    
    #Second phase
    bounds = [[-20, 20], [-16, 16], [-10, 10]]
    spacing = [4,2,1]
    
    #Getting data in both directions
    k = 0
    delta = 45
    saved_data = [] #Saves the data for future visualization
    while k < 3 and delta > tol:
        #Prepares which coordinates are to be measured
        ele = np.arange(bounds[k][0] + max_position, bounds[k][1] + max_position+1, spacing[k])
        data_ele = np.zeros_like(ele, dtype = 'float32')

        #Measure in elevation
        for j in range(len(ele)):
            data_ele[j] = func(ele[j])

        #Put all data in one array
        data = []
        for j in range(len(ele)):
            data.append([ele[j], data_ele[j]])
        data = np.array(data)
        for i in range(len(data)):
            saved_data.append(data[i])

        #Error function to minimize
        error = lambda x: MeanSquare2D(np.zeros_like(data[:,0]), data[:,0], data[:,1], modelfunc, 0, x)

        #The initial estimate x0 is made of the current maximum power measured
        index = np.argmax(data_ele)
        ele0 = ele[index] - max_position
        x0 = ele0
        print("Best measured elevation = "+str(x0 + max_position))

        #Minimizing the error model from x0 with the Nelder-Mead heuristic to a certain tolerance
        res = minimize(error, x0, method = 'Nelder-Mead', tol = 10**-1)
        print("Regression iteration = "+str(k+1)+"\t x = "+str(res.x + max_position)+"\t f = "+str(res.fun))
        best_ele = res.x

        max_position = max_position + np.round(best_ele)
        k += 1
        #Realign with new best position
        func(max_position)
    return max_position, np.array(saved_data)

if __name__ == '__main__':
    import time
    
    start_time = time.time()
    complete_model, power_detector, motor_arduino, TCPsocket, compass = init(datasets_directory = "datasets/Domain/", COM_Power = 'COM9', COM_Motor = 'COM7', COM_compass = 'COM10') #Initializing all components

    func = lambda ele: partialGetPower(0, ele, power_detector, motor_arduino, TCPsocket, 'AntennaControl\Antenna_control_phase_steps_1deg_resolution.txt') #Function to get the power at particular position
    func(0) #Initialize system's position
    best_ele, data = single_detect(func, complete_model, tol = 10**-3) #Find the position of the system

    end_time = time.time()
    print("Temps = "+str(end_time-start_time))

    #Print the source's position
    print("Best elevation = "+str(best_ele))