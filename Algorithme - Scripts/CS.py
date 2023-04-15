#Algorithme de recherche par coordonnées (CS)

import numpy as np

def opportunisticCS(func, x0, tol = 10**-3, neval = 100, tau = 0.5):
    #Initialisation
    delta = 1
    f = func(x0)
    k = 0 #Iteration counter
    
    #Getting global directions
    n = len(x0)
    In = np.eye(n)
    D = np.hstack((In, -In))
    e = []
    for i in range(2*n):
        ei = D[:,i]
        e.append(ei)
    
    while delta > tol and k < neval:
        
        fail = True
        for i, ei in enumerate(e):
            k += 1
            xi = x0 + delta*ei
            fi = func(xi)
            # Opportunistic and dynamic coordinates
            if fi < func(x0):
                x0 = xi
                delta = np.min([delta/tau, 4])
                fail = False
                del e[i]
                e.insert(0, ei)
                break
        if fail == True:
            delta = np.max([delta*tau, 0.5])
    return x0