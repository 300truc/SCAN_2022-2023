#Unit test for gridsearch

from IntegratedDetection import *

if __name__ == '__main__':
    complete_model, power_detector, motor_arduino, TCPsocket, compass = init(datasets_directory = "datasets/Domain/", COM_Power = 'COM5', COM_Motor = 'COM7', COM_compass = 'COM9') #Initializing all components

    func = lambda azi, ele: getPower(azi, ele, power_detector, motor_arduino, TCPsocket, 'AntennaControl\Antenna_control_phase_steps_1deg_resolution.txt')
    func(0, 0)
    positions, powers = gridsearch(lambda x: func(x[0], x[1]), [-180, -30], [180, 30], [9, 3], current_position = [0,0])
    
    max_index = np.argmax(powers)
    max_position = positions[max_index]
    func(max_position[0], max_position[1])
    
    print("Positions:")
    print(positions)

    print("Powers:")
    print(powers)

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter(positions[:,0], positions[:,1], powers)
    ax.set_xlabel('A [°]')
    ax.set_ylabel('h [°]')
    plt.show()