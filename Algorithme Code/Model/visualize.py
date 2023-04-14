#Visualizing the radiation patterns in 2D contours and 3D plots

import matplotlib.pyplot as plt

def showPattern(A, H, P):
    fig, ax = plt.subplots()
    contour = plt.contourf(A, H, P, levels = 100, cmap = 'rainbow')
    plt.xlabel('A')
    plt.ylabel('h')
    cbar = plt.colorbar(contour)
    cbar.set_label('P')
    
def showPoints(data):
    ax = plt.figure().add_subplot(projection='3d')
    for i in range(len(data)):
        if data[i,1] == -26:
            ax.scatter(data[i,0], data[i,2], data[i,3], c='C0')
    plt.xlabel('A')
    plt.ylabel('h')