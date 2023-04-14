#Unit test for reading the power output

from IntegratedDetection import *

if __name__ == '__main__':
    power_detector = serial.Serial('COM5')

    n = 20
    p = np.zeros(n)
    i = 0
    while i<n:
        
        p[i] = (readPower(power_detector))
        i+=1

    plt.figure()
    plt.plot(np.arange(0, n, 1), p)
    plt.xlabel('Evaluation number')
    plt.ylabel('P [dB]')
    plt.title('Power according to evaluation')
    plt.show()