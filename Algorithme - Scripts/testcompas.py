from IntegratedDetection import *

if __name__ == '__main__':
    compass = serial.Serial('COM9')

    n = 20
    p = np.zeros(n)
    i = 0
    while i<n:
        
        p[i] = (readCompassAngle(compass))
        i+=1
    
    moy_angle = p[8:].mean()
    print(moy_angle)

    plt.figure()
    plt.plot(np.arange(8, n, 1), p[8:])
    plt.xlabel('Evaluation number')
    plt.ylabel('P [dB]')
    plt.title('Power according to evaluation')
    plt.show()