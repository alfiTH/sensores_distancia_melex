import socket
import sys
import time

def include_dic( dic, add):
    for sen in add:
        sensor = sen.split(";")
        if sensor[0] != "" :
            print('received =', sensor)
            dic[sensor[0]] = sensor[1::1]

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('158.49.247.198', 2014)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)
server_address = ('158.49.247.198', 2001)
print('connecting to {} port {}'.format(*server_address))
sock2.connect(server_address)

try:

    # Send data
    #message = b'This is the message.  It will be repeated.'
    # print('sending {!r}'.format(message))
    # sock.sendall(message)

    # Look for the response
    #amount_received = 0
    # amount_expected = len(message)
    sensores = {}
    while(True): 
        start_time = time.time()
        #amount_received += len(data)
        sensor_sin = sock.recv(1024).decode().split(":")
        include_dic (sensores, sensor_sin)
        sensor_sin = sock2.recv(1024).decode().split(":")
        include_dic (sensores, sensor_sin)
    
        print('sensores =', sensores)
        print("--- %s seconds ---" % (time.time() - start_time))
       # print(sensor[0], sensor[1])

finally:
    print('closing socket')
    sock.close()


