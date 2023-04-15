#Unit test for the whole detection without hardware

from IntegratedDetection import *

import numpy as np

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
    
    func = lambda azi, ele: artificialGetPower(complete_model, azi, ele, -90, 10) #Function to get the power at particular position artificially
    best_azi, best_ele, data = detect(func, [-180, -30], [180, 30], [9, 3], complete_model, tol = 10**-3) #Find the position of the system

    #Plot the detection pattern (optional)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter(data[:,0], data[:,2], data[:,3])
    ax.set_xlabel('A [°]')
    ax.set_ylabel('h [°]')
    plt.show()

    #Print the source's position
    print("Best azimuth = "+str(best_azi)+"\t Best elevation = "+str(best_ele))