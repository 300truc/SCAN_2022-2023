#Fonction de calcul de l'erreur quadratique moyenne

import numpy as np

def MeanSquare1D(xtest, ztest, model, shift):
    error = 0
    for i in range(len(xtest)):
        zmodel = model(xtest[i] - shift)
        error += (((ztest[i]-zmodel))**2)*np.exp(ztest[i]) #Ajout d'importance aux données haute puissance (en positif, négatif seront diminuées)
    return error/len(xtest)

def MeanSquare2D(xtest, steerings, ztest, model, AziShift, EleShift):
    #xtest: Coordonnées de validation
    #ytest: Coordonnées de validation
    #ztest: Données de validation
    #model: Fonction modèle retournant une valeur yhat = f(xtest-shift) (bestfit)
    #       Doit être un objet de la classe model
    #shift: Décalage testé
    error = 0
    for i in range(len(xtest)):
        zmodel = model.eval([xtest[i] - AziShift, -EleShift, steerings[i]])
        error += (((ztest[i]-zmodel))**2)#*np.exp(ztest[i]) #Ajout d'importance aux données haute puissance (en positif, négatif seront diminuées)
    return error/len(xtest)