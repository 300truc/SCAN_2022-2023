#Performs a gridsearch algorithm

import numpy as np

def gridsearch(func, lower_bounds, upper_bounds, p, initial_position = [0,0]):
    """Performs a grid search on an hyper-rectangle as presented in Audet & Hare "Derivative free and black-box optimisation". This is applied to a 2D problem

    Args:
        func (function): Objective function
        lower_bounds (list): Array of lower bounds on input variables
        upper_bounds (list)): Array of upper bounds on input variables
        p (list): Number of points allowed per variable
        initial_position (list): Initial position to return afterwards
    """
    total_points = np.product(p)
    X = np.zeros([total_points, len(p)])
    f = np.empty(total_points)
    k = 0
    delta_1 = (upper_bounds[0] - lower_bounds[0])/(p[0]-1)
    delta_2 = (upper_bounds[1] - lower_bounds[1])/(p[1]-1)
    delta = [delta_1, delta_2]
    for j in range(p[0]): #On the first axis
        for i in range(p[1]): #On the second axis
            x = lower_bounds[0] + j*delta[0]# + (j%2 != 0)*delta[0]/2
            y = lower_bounds[1] + i*delta[1]
            X[k,0] = x
            X[k,1] = y
            f[k] = func([x,y])
            k += 1
    func([initial_position[0], initial_position[1]])
    return X, f
        
    

if __name__ == '__main__':
    l = np.array([-180, 10])
    u = np.array([180, 70])
    n = 2
    p = [9, 3]
    
    X, f = gridsearch(lambda x: 0, l, u, p)
    
    import matplotlib.pyplot as plt
    
    fig, axs = plt.subplots()
    
    # circle = lambda t, xi, yi: [xi+(45/2)*np.cos(t), yi+(45/2)*np.sin(t)]
    # index = lambda i,j: i*p[1] + j
    # for i in range(p[0]):
    #     for j in range(p[1]):
    #         t = np.linspace(0, 2*np.pi, 1000)
    #         x,y = np.zeros(len(t)), np.zeros(len(t))
    #         for k in range(len(t)):
    #             x[k],y[k] = circle(t[k], X[index(i,j),0], X[index(i,j),1])
    #         plt.plot(x,y,'k')
    
    plt.scatter(X[:,0], X[:,1], label = 'Grid')
    plt.xlabel("Azimut [°]")
    plt.ylabel("Élévation [°]")
    axs.set_aspect('equal', 'box')
    axs.set_xticks([-180, -120, -60, 0, 60, 120, 180])
    axs.set_yticks([10, 30, 50, 70])
    plt.xlim([-180, 180])
    plt.ylim([10,70])
    plt.show()