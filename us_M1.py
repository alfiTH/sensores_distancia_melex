#!/usr/bin/python3
from time import sleep
import serial
import socket
import time
import sys

tempo = 0.09

f = open(sys.argv[1])
port = int(f.readline())
dispositivos = f.readline().split(';')
print(dispositivos)



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('158.49.247.198', port)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)





# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:

        print('connection from', client_address)
        print(dispositivos)
        serials=[]
        for d in dispositivos[1::2]:
            print(d)
            ser = serial.Serial(
                        port=str(d),
                        baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=0
                    )
            #ser.flushInput()
            if ser.isOpen():
                serials.append(ser)
                print(d, " arrancado")
        
        start_time = time.time()
        while(True):
            sendata = ""
            for s in range(len(serials)):
                stringDistance =serials[s].readline()
                #print(stringDistance)
                if len(stringDistance)>4:
                    tempo-=0.00001
                elif len(stringDistance)<4:
                    tempo+=0.00001
                elif stringDistance[0] == 255:  
                    if (stringDistance[2]+stringDistance[1]+stringDistance[0])%256 != stringDistance[3]:
                        print("**********ERROR CHECKSUM************")
                    else:
                        distance = stringDistance[2] + stringDistance[1]*255
                        print(dispositivos[s*2], ' distance =', distance)
                        sendata = sendata + str(dispositivos[s*2]) + ";" + str(distance) + ":"

            if sendata != "":
                print("send", sendata)
                connection.send(sendata.encode())
                print("--- %s seconds ---" % (time.time() - start_time)) 
                start_time = time.time()
            sleep(tempo)
            #print("temporizador de buffer ", tempo)
    except:
        # Clean up the connection
        print(sys.exc_info()[0])
        
        for s in serials:
            print ("cerramos ", s)
            s.close()

        print("cerramos ", connection)
        connection.close()
    