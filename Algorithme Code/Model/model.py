#Create the model that interpolates the data obtained through tests

import numpy as np
from scipy.interpolate import LinearNDInterpolator
from scipy.ndimage import uniform_filter
from .getData import *
from .visualize import *

class model:    
    #Dataset when only in one steering
    def build_3Ddataset(self, filename, size = 3):
        name = filename.split('_')
        self.e = int(name[3])
        self.A, self.H, self.P = get_3Ddataset(filename)
        self.filteredP = uniform_filter(self.P, size = size, mode = 'nearest')
        self.dataset = get_points(np.array([self.A]), np.array([self.H]), np.array([self.e]), np.array([self.filteredP]))
    
    #Dataset with multiple steerings - most likely the one used
    def build_4Ddataset(self, filenames, size = 3, mode = 'somme', f = '28.'):
        self.A, self.H, self.e, self.P = get_4Ddataset(filenames, mode, f)
        self.filteredP = []
        for i in range(len(self.P)):
            self.filteredP.append(uniform_filter(self.P[i], size = size, mode = 'nearest'))
        self.dataset = get_points(self.A, self.H, self.e, self.filteredP)
    
    def save_dataset(self, filename = 'model.txt'):
        np.savetxt(filename, self.dataset)

    def load_dataset(self, filename = 'model.txt'):
        self.dataset = np.loadtxt(filename)

    def build_interpolator(self):
        #dataset: Array of [azimuts, elevations, steerings, powers]
        dataset = self.dataset
        self.f = LinearNDInterpolator(dataset[:,:3], dataset[:,3], fill_value = np.min(dataset[:,3]))
        #If the value to interpolate is outside the existing data, we give it the minimum value of the data
        #Thus, this returns the ambient noise
    
    def eval(self, x):
        #Evaluate the interpolation model
        return self.f(x)
    
    def show(self): #Used for debugging with a 3D dataset
        showPattern(self.A, self.H, self.filteredP)
    
if __name__ == '__main__':
    import os
    complete_model = model()
    files = os.listdir(r'datasets\domain')
    for i, file in enumerate(files):
        files[i] = r'datasets\\domain\\'+file


    complete_model.build_4Ddataset(files)
    complete_model.build_interpolator()
    #from visualize import *

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    n = 50
    azi = np.linspace(-180, 180, n)
    ele = np.linspace(-30, 30, n)
    data = []
    for i in range(n):
        for j in range(n):
            data.append([azi[i], ele[j], complete_model.eval([azi[i] - 100, 30, ele[j]])[0]])
    data = np.array(data)
    
    ax.scatter(data[:, 0], data[:, 1], data[:, 2])
    ax.set_xlabel('A [°]')
    ax.set_ylabel('h [°]')
    plt.show()
    exit()
    index = int(np.where(complete_model.e == 10)[0])
    
    #showPoints(complete_model.dataset)
    showPattern(complete_model.A[index], complete_model.H[index], complete_model.P[index])
    showPattern(complete_model.A[index], complete_model.H[index], complete_model.filteredP[index])
    
    import matplotlib.pyplot as plt

    plt.figure()
    #Plotting the A=0° H=0° curve for different e
    e = np.linspace(-10,10,50)
    P = np.zeros(len(e))
    for i in range(len(e)):
        x = [0,0,e[i]]
        P[i] = complete_model.eval(x)
    plt.plot(e,P)
    plt.xlabel('Steering')
    plt.ylabel('Power')    
    plt.show()