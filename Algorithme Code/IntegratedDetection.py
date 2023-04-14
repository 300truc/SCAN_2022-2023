#Main function file for detection

from Model.getData import *
from Model.model import *
from Model.visualize import *
from Model.MeanSquare import *
from prebrute import *
import serial
from AntennaControl.BBoard_control import *
from AntennaControl.Read_txt import *
import socket
import time
from scipy.optimize import minimize

#System initialization
def init(datasets_directory, COM_Power, COM_Motor, COM_compass):
    #Detection model
    complete_model = model()
    
    #If the model has been initialized in the past, directly load the dataset
    complete_model.load_dataset()
    
    #If the model has not been initialized, uncomment and save the dataset for future use (improved efficiency)
    #import os
    #files = os.listdir(datasets_directory)
    #for i, file in enumerate(files):
    #   files[i] = datasets_directory+file
    #complete_model.build_4Ddataset(files)
    #complete_model.save_dataset()
    
    #Building an interpolator for greater resolution
    complete_model.build_interpolator()

    #Initializing the compass
    compass = serial.Serial(COM_compass)    

    #Initializing power detector
    power_detector = serial.Serial(COM_Power)
    
    #Initializing the motor and keeping track of its position
    with open('currentpos.txt', 'w') as file:
        file.write('0')
    motor_arduino = serial.Serial(COM_Motor, 115200)

    #Initializing the antenna through the BBoard (inspired from the software given by TMYTEK through Prof. Jean-Jacques Laurin)
    RECV_TIMEOUT = 15
    IP = "192.168.100.111"
    PORT = 5025
    try:
        TCPsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPsocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        TCPsocket.settimeout(RECV_TIMEOUT)
        TCPsocket.connect((IP, PORT))
        SendCmdThenWaitRSP(TCPsocket,"INIT 0 \n\r",0)
        SendCmdThenWaitRSP(TCPsocket,"TDD 2 \n\r",0) # TDD 1 in TX, 2 in RX
    except socket.error as msg:
            print('[Init_TCP_client]Exception : %s' % (msg))
    
    return complete_model, power_detector, motor_arduino, TCPsocket, compass

#Sending a command to the motor
def motorCommand(arduino, angle_deg):
    with open('currentpos.txt', 'r') as file:
        current_pos = float(file.readline())
    
    arduino.write((str(angle_deg - current_pos)+"\r").encode())
    
    current_pos = angle_deg
    with open('currentpos.txt', 'w') as file:
        file.write(str(current_pos))
    
#Sending a command to the antenna (inspired from the software given by TMYTEK through Prof. Jean-Jacques Laurin)
def steer(angle_deg, mode, antenna_socket, filename):
    somme, difference = Read_txt(filename)
    for i in range(len(somme)):
        if somme[i,0] == angle_deg and mode == "somme":
            SendCmdThenWaitRSP(antenna_socket,"MODULE_CTRL_ 1,2,0,0,0,0,0,"+str(somme[i,1])+","+str(somme[i,2])+","+str(somme[i,3])+","+str(somme[i,4])+",0,0,3,5,0 \n\r",0)
            break
        if difference[i,0] == angle_deg and mode == "difference":
            SendCmdThenWaitRSP(antenna_socket,"MODULE_CTRL_ 1,2,0,0,0,0,0,"+str(difference[i,1])+","+str(difference[i,2])+","+str(difference[i,3])+","+str(difference[i,4])+",0,0,3,5,0 \n\r",0)
            break

#Reading the power through the power detector.    
def readPower(power_detector, n=10):
    #The power detector sometimes crashes, in this case, try again         
    try:
        powers = np.zeros(n)
        #Use a mean of n power measures for better accuracy
        for i in range(n):
            powers[i] = power_detector.readline().decode()
        p = powers.mean()
        #Sometimes, the power detector returns illogical values. In this case, try again
        #Typical noise values are expected to be at the minimum -37dB
        if p < -40:
            return readPower(power_detector, n)
        return p
    except:
        print("Crashed, trying again")
        return readPower(power_detector, n)

def readCompassAngle(compass, n=20):
    try:
        angle = np.zeros(n)
        for i in range(n):
            angle[i] = compass.readline().decode()
        p = angle[10:].mean()
 #       if p < 0:
  #          return readCompassAngle(compass, n)
        return p
    except:
        print("Crashed, trying again")
        return readCompassAngle(compass, n)
    
def initPositionAz(compass, angle_initial, motor_arduino):
    n = 20
    p = np.zeros(n)
    i = 0
    while i<n:
        
        p[i] = (readCompassAngle(compass))
        i+=1
    
    moy_angle = p[8:].mean()
    #moy_angle = 320
    if moy_angle-angle_initial<180 and moy_angle-angle_initial > -180:
        position_sys = moy_angle-angle_initial
    else:
        position_sys = moy_angle-angle_initial+360
        
    with open('currentpos.txt', 'w') as file:
        file.write(str(0))
    motorCommand(motor_arduino, position_sys)
    with open('currentpos.txt', 'w') as file:
        file.write(str(0))
    return position_sys

#Integrate the motor, antenna and power detector together
def getPower(azi, ele, power_detector, motor_arduino, antenna_socket, filename, RPM = 30):
    with open('currentpos.txt', 'r') as file:
        current_pos = float(file.readline())
        incr = azi - current_pos
    motorCommand(motor_arduino, azi)
    
    #The wait time depends on the motor's speed
    #While the motor is moving, take measures and send commands, but do not store these values
    start = time.time()
    while time.time() - start <= 2*abs(incr/360)/(RPM/60) + 1:
        steer(ele, 'somme', antenna_socket, filename)
        power = readPower(power_detector, 30)
        
    #Printing the results for ease of debugging and information tracking
    print('Azimut = '+str(azi)+'\t Elevation = '+str(ele)+'\t Power = '+str(power))
    return power

#Integrate the whole detection algorithm within one function
def detect(func, lower, upper, npoints, modelfunc, tol = 10**-3, initial_position = [0,0]):
    #Perform the prebrute search
    positions, powers = gridsearch(lambda x: func(x[0], x[1]), lower, upper, npoints, initial_position = initial_position)
    
    #First estimate is the maximum power measured yet
    max_index = np.argmax(powers)
    max_position = positions[max_index]
    func(max_position[0], max_position[1])
    
    #Second phase
    bounds = [[-20, 20], [-16, 16], [-10, 10]]
    spacing = [4,2,1]
    
    #Getting data in both directions
    k = 0
    delta = 45
    saved_data = [] #Saves the data for future visualization
    while k < 3 and delta > tol:
        #Prepares which coordinates are to be measured
        azi = np.arange(bounds[k][0] + max_position[0], bounds[k][1] + max_position[0]+1, spacing[k])
        ele = np.arange(bounds[k][0] + max_position[1], bounds[k][1] + max_position[1]+1, spacing[k])
        data_azi = np.zeros_like(azi, dtype = 'float32')
        data_ele = np.zeros_like(ele, dtype = 'float32')

        #Measure in azimut
        for i in range(len(azi)):
            data_azi[i] = func(azi[i], max_position[1])
        #Return to initial position
        func(max_position[0], max_position[1])
        #Measure in elevation
        for j in range(len(ele)):
            data_ele[j] = func(max_position[0], ele[j])

        #Put all data in one array
        data = []
        for i in range(len(azi)):
            data.append([azi[i], 0, max_position[1], data_azi[i]])
        for j in range(len(ele)):
            data.append([max_position[0], 0, ele[j], data_ele[j]])
        data = np.array(data)
        for i in range(len(data)):
            saved_data.append(data[i])

        #Error function to minimize
        error = lambda x: MeanSquare2D(data[:,0], data[:,2], data[:,3], modelfunc, x[0], x[1])

        #The initial estimate x0 is made of the current maximum power measured
        index = np.argmax(data_azi)
        azi0 = azi[index] - max_position[0]
        index = np.argmax(data_ele)
        ele0 = ele[index] - max_position[1]
        x0 = [azi0, ele0]
        print("Best measured azimut = "+str(x0[0] + max_position[0])+"\t Best measured elevation = "+str(x0[1] + max_position[1]))

        #Minimizing the error model from x0 with the Nelder-Mead heuristic to a certain tolerance
        res = minimize(error, x0, method = 'Nelder-Mead', tol = 10**-1)
        print("Regression iteration = "+str(k+1)+"\t x = "+str(res.x + max_position)+"\t f = "+str(res.fun))
        best_azi = res.x[0]
        best_ele = res.x[1]

        max_position = [max_position[0] + best_azi, max_position[1] + np.round(best_ele)]
        k += 1
        #Realign with new best position
        func(max_position[0], max_position[1])
    return max_position[0], max_position[1], np.array(saved_data)