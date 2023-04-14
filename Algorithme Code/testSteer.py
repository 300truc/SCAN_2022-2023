#Unit test for controlling the antenna

from IntegratedDetection import *

def partialGetPower(azi, ele, power_detector, motor_arduino, antenna_socket, filename, RPM = 10, mode='somme', f = 28E9):
    motorCommand(motor_arduino, azi)
    steer(ele, mode, antenna_socket, filename, f)
    power = readPower(power_detector, 15)
    print(ele, power)
    return power

if __name__ == '__main__':
    power_detector = serial.Serial('COM9')
    motor_arduino = serial.Serial('COM7')
    print("essai")

    #Commande de l'antenne
    RECV_TIMEOUT = 15
    IP = "192.168.100.111"
    PORT = 5025
    try:
        TCPsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPsocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        TCPsocket.settimeout(RECV_TIMEOUT)
        TCPsocket.connect((IP, PORT))
        SendCmdThenWaitRSP(TCPsocket,"INIT 0 \n\r",0)
        SendCmdThenWaitRSP(TCPsocket,"TDD 2 \n\r",0) # TDD 1 in TX, 2 in RX
    except socket.error as msg:
            print('[Init_TCP_client]Exception : %s' % (msg))

    a = np.linspace(-30, 30, 61)
    ps = np.zeros_like(a)
    pdi = np.zeros_like(a)
    for i, ai in enumerate(a):
         ps[i] = partialGetPower(0, ai, power_detector, motor_arduino, TCPsocket, filename = 'AntennaControl\Antenna_control_phase_steps_1deg_resolution.txt', mode='somme', f = 27.5E9)
         pdi[i] = partialGetPower(0, ai, power_detector, motor_arduino, TCPsocket, filename = 'AntennaControl\Antenna_control_phase_steps_1deg_resolution.txt', mode = 'somme', f = 28.5E9)

    plt.figure()
    plt.plot(a, ps)
    plt.xlabel('h [°]')
    plt.ylabel('P [dB]')
    plt.title('Power against electronic steering')
    
    plt.figure()
    plt.plot(a, pdi)
    plt.xlabel('h [°]')
    plt.ylabel('P [dB]')
    plt.title('Power against electronic steering')
    
    plt.figure()
    plt.plot(a, ps-pdi)
    plt.xlabel('h [°]')
    plt.ylabel('P [dB]')
    plt.title('Power against electronic steering')
    plt.show()
    
    