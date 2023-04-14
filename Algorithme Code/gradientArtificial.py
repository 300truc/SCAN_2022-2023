#Gradient detection for satellite following

import numpy as np
from IntegratedDetection import *

def simplex_gradient(func, x0, delta):
    n = len(x0)
    grad = np.zeros(n)
    for i in range(n):
        step = np.zeros(n)
        step[i] = delta
        fi = func(x0 + step)
        fj = func(x0 - step)
        grad[i] = (fi - fj)/(2*delta)
    return grad

def gradient_optimizer(func, x0, tol, n, tau = 0.5):
    k = 0
    delta = 1
    f = func(x0)
    while k <=n and delta > tol:
        d = -simplex_gradient(func, x0, delta)
        if np.linalg.norm(d) < tol:
            return x0
        k += 1
        fi = func(x0 + delta*d)
        if fi < f:
            f = fi
            x0 += delta*d
            delta = delta/tau
        else:
            delta = delta*tau
            
    return x0

def ArtificialInit(datasets_directory):
    #Detection model
    complete_model = model()
    
    #If the model has been initialized in the past, directly load the dataset
    complete_model.load_dataset()
    
    #If the model has not been initialized, uncomment and save the dataset for future use (improved efficiency)
    # import os
    # files = os.listdir(datasets_directory)
    # for i, file in enumerate(files):
    #  files[i] = datasets_directory+file
    # complete_model.build_4Ddataset(files)
    # complete_model.save_dataset()
    
    #Building an interpolator for greater resolution
    complete_model.build_interpolator()
    return complete_model

import time
def artificialGetPower(model_data, azi, ele, azi_shift, ele_shift):
    power = model_data.eval([azi-azi_shift, ele_shift, ele]) + np.random.uniform(-0.25, 0.25)
    print('Azimut = '+str(azi)+'\t Elevation = '+str(ele)+'\t Power = '+str(power))
    return power

if __name__ == '__main__':
    complete_model = ArtificialInit(datasets_directory = "datasets/Domain/") #Initializing all components
    
    power = lambda azi, ele: artificialGetPower(complete_model, azi, ele, -90, 10) #Function to get the power at particular position artificially
    x0 = gradient_optimizer(lambda x0: -1*power(x0[0], x0[1]), x0 = [-80, 10], tol = 0, n = float('inf')) #Find the position of the system

    #Print the source's position
    print("Best azimuth = "+str(x0[0])+"\t Best elevation = "+str(x0[1]))
    