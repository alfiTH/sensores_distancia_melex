import socket
import time
from multiprocessing import Process, Manager

def com_socket (ip, puerto, dic):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    server_address = (ip, puerto)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)
    try:
        while True:
            sensor_sin = sock.recv(1024).decode().split(":")
            include_dic (dic, sensor_sin)
    finally:
        print('closing socket')
        sock.close()

def include_dic( dic, add):
    for sen in add:
        sensor = sen.split(";")
        if sensor[0] != "" :
            #print('received =', sensor)
            dic[sensor[0]] = sensor[1::1]


if __name__ == '__main__':
    with Manager() as manager:
        #creamos dicionario
        sensores = manager.dict()
        #creamos procesos de comunicación por socket
        p = Process(target=com_socket, args=('127.0.0.1', 2015,sensores))
        p2 = Process(target=com_socket, args=('127.0.0.1', 2001,sensores))
        #arrancamos los procesos
        p.start()
        p2.start()
        while(True): 
            # start_time = time.time()  
            print('sensores =', sensores)
            time.sleep(0.02)
            #print("--- %s seconds ---" % (time.time() - start_time))





