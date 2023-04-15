#Unit test for the whole detection without hardware with the quotient model

from IntegratedDetection import *

import numpy as np

def ArtificialInit(datasets_directory, mode):
    #Detection model
    complete_model = model()
    
    #If the model has been initialized in the past, directly load the dataset
    #complete_model.load_dataset()
    
    #If the model has not been initialized, uncomment and save the dataset for future use (improved efficiency)
    import os
    files = os.listdir(datasets_directory)
    for i, file in enumerate(files):
     files[i] = datasets_directory+file
    complete_model.build_4Ddataset(files, mode = mode)
    #complete_model.save_dataset()
    
    #Building an interpolator for greater resolution
    complete_model.build_interpolator()
    return complete_model

def single_detect(func, x0, modelfunc, tol = 10**-3):
    #Second phase
    bounds = [[-20, 20], [-16, 16], [-10, 10]]
    spacing = [4,2,1]
    
    #Getting data in both directions
    k = 0
    delta = 45
    saved_data = [] #Saves the data for future visualization
    while k < 3 and delta > tol:
        #Prepares which coordinates are to be measured
        scan = np.arange(bounds[k][0] + x0, bounds[k][1] + x0+1, spacing[k])
        data_scan = np.zeros_like(scan, dtype = 'float32')

        for i in range(len(scan)):
            data_scan[i] = func(scan[i])

        for i in range(len(scan)):
            saved_data.append([scan[i], data_scan[i]])

        #Error function to minimize
        error = lambda x: MeanSquare1D(scan, data_scan, modelfunc, x)

        #The initial estimate x0 is made of the current maximum power measured
        index = np.argmax(data_scan)
        xbest = scan[index] - x0
        print("Best measured scan angle = "+str(xbest + x0))

        #Minimizing the error model from x0 with the Nelder-Mead heuristic to a certain tolerance
        res = minimize(error, xbest, method = 'Nelder-Mead', tol = 10**-1)
        print("Regression iteration = "+str(k+1)+"\t x = "+str(res.x + x0)+"\t f = "+str(res.fun))
        best_shift = res.x[0]
        
        x0 += best_shift
        k += 1
    return x0, np.array(saved_data)

def artificialGetPower(model_data, azi, ele, azi_shift, ele_shift):
    power = model_data.eval([azi-azi_shift, ele_shift, ele])# + np.random.uniform(-0.25, 0.25)
    print('Azimut = '+str(azi)+'\t Elevation = '+str(ele)+'\t Power = '+str(power))
    return power

if __name__ == '__main__':
    print("Initializing summation model")
    const_model = ArtificialInit(datasets_directory = "datasets/Domain/", mode = 'somme') #Initializing all components
    print("Initializing difference model")
    diff_model = ArtificialInit(datasets_directory = "datasets/Domain/", mode = 'difference')
    
    
    azi_shift = -60
    ele_shift = 20
    
    const = lambda azi, ele: artificialGetPower(const_model, azi, ele, azi_shift, ele_shift) #Function to get the power at particular position artificially
    diff = lambda azi, ele: artificialGetPower(diff_model, azi, ele, azi_shift, ele_shift) #Function to get the power at particular position artificially
    
    print("Gridsearch")
    positions, powers = gridsearch(lambda x: const(x[0], x[1]), [-180, -30], [180, 30], [9,3], initial_position = [0,0])
    
    #First estimate is the maximum power measured yet
    max_index = np.argmax(powers)
    max_position = positions[max_index]
    
    print("Elevation detection")
    best_ele, data = single_detect(lambda x: const(max_position[0], x) - diff(max_position[0], x), max_position[1], lambda x: const_model.eval([max_position[0], x, x]) - diff_model.eval([max_position[0], x, x]), tol = 10**-3) #Find the position of the system
    
    #Plot the detection pattern (optional)
    fig = plt.figure()
    plt.scatter(data[:,0], data[:,1])
    plt.xlabel('h[°]')
    plt.ylabel('P [dBm]')
    plt.show()
    
    print("Azimut detection")
    best_azi, data = single_detect(lambda x: const(x, best_ele), max_position[0], lambda x: const_model.eval([x, best_ele, best_ele]), tol = 10**-3) #Find the position of the system

    #Plot the detection pattern (optional)
    fig = plt.figure()
    plt.scatter(data[:,0], data[:,1])
    plt.xlabel('h[°]')
    plt.ylabel('P [dBm]')
    plt.show()

    #Print the source's position
    print("Best azimuth = "+str(best_azi)+"\t Best elevation = "+str(best_ele))