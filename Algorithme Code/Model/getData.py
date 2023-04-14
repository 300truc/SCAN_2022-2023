#Read the test data

import numpy as np
import pandas as pd

def get_3Ddataset(filename):
    data_test = ReadExcel(filename)
    
    azimuts = np.unique(data_test[:,0])
    elevations = np.unique(data_test[:,1])
    A, H = np.meshgrid(azimuts, elevations, indexing = 'ij')
    
    P = np.zeros([len(azimuts), len(elevations)])
    
    for k, p in enumerate(data_test[:,2]):
        a = data_test[k,0]
        h = data_test[k,1]
        
        i = np.where(azimuts == a)
        j = np.where(elevations == h)
        
        P[i,j] = p
    return A, H, P

def get_4Ddataset(filenames):
    #All the datasets must have the same azimuts and elevations
    data_test = ReadExcel(filenames[0])
    
    e = []
    for filename in filenames:
        name = filename.split('_')
        e.append(int(name[1][:-3]))
    e = np.unique(np.array(e))
    
    P = []
    A = []
    H = []
    
    for k in range(len(e)):
        filename = None
        for file in filenames:
            name = file.split('_')
            if int(name[1][:-3]) == e[k]:
                filename = file
                if name[2] == 'const':
                    break
        Ak, Hk, Pk = get_3Ddataset(filename)
        Pc = Pk
        A.append(Ak)
        H.append(Hk)
        for file in filenames:
            name = file.split('_')
            if int(name[1][:-3]) == e[k]:
                filename = file
                if name[2] == 'dest':
                    break
        Ak, Hk, Pk = get_3Ddataset(filename)
        Pd = Pk
        P.append(Pc)
    return A, H, e, P

def get_points(A, H, e, P):
    #Converts A, H, P matrices to a list of data points
    #datapoint = [azimut, elevation, steering, power]
    datapoints = []
    for k in range(len(e)):
        Pi = P[k]
        Ai = A[k]
        Hi = H[k]
        for j in range(len(Pi[0,:])):
            for i in range(len(Pi[:,0])):
                datapoints.append(np.array([Ai[i,j], Hi[i,j], e[k], Pi[i,j]]))
    return np.array(datapoints)

#Excel reading function, taken from given code by Maxime Thibault
def ReadExcel(txt):
    header = pd.read_excel(txt, index_col=None, sheet_name='Header')
    STEP_START = header.iat[2,1]
    STEP_STOP = header.iat[2,2]
    STEP_INC = header.iat[2,3]
    SCAN_START = header.iat[3,1]
    SCAN_STOP = header.iat[3,2]
    SCAN_INC = header.iat[3,3]
    data = pd.read_excel(txt, index_col=None, sheet_name='28.')
    angle_azimut = np.array(STEP_INC*data['Scan']+STEP_START-STEP_INC-90)
    angle_elevation = np.array(SCAN_INC*data['Rinc']+SCAN_START-SCAN_INC)
    Puissance_lue = np.array(data['Bin1Amptd'])
    dataset_constructif_0_balayage = np.array([angle_azimut, angle_elevation, Puissance_lue]).T

    return dataset_constructif_0_balayage