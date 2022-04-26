#!/usr/bin/python3
from time import sleep
import serial
import socket
import time
import sys

tempo = 0.0087

#leemos configuración
f = open(sys.argv[1])
port = int(f.readline())
dispositivos = f.readline().split(';')
print(dispositivos)

#preparamos socket
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
        serials=[]
        #abrimos serials
        for d in dispositivos[1::2]:
            ser = serial.Serial(
                        port=str(d),
                        baudrate=115200,
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
             #leemos todos los serials
            for s in range(len(serials)):
                ##leemos
                stringDistance =serials[s].readline()
                #print(stringDistance)
                if len(stringDistance)>9:
                    tempo-=0.00001
                elif len(stringDistance)<9:
                    tempo+=0.00001
                elif stringDistance[0] == stringDistance[1] and stringDistance[0] == 89:
                    if ((sum(stringDistance)-stringDistance[8])%256) != stringDistance[8]:
                        print("**********ERROR CHECKSUM************")
                    else:
                        luz = stringDistance[4] + stringDistance[5]*255
                        if (100>luz or luz==65535):
                            print("************ERROR DE LUZ*********")
                        else:
                            distance = (stringDistance[2] + stringDistance[3]*255)*10
                            tem = (stringDistance[6] + stringDistance[7]*255)/100
                            print(dispositivos[s*2],' data: distance =', distance," exposure =", luz," temperature =", tem)
                            #formato IDsensor1;DistanciasSensor1;exposicionSensor1;TemperaturaSensor1:IDsensorn;DistanciasSensorn;exposicionSensorn;TemperaturaSensorn:
                            sendata = sendata + str(dispositivos[s*2]) + ";" + str(distance) + ";" + str(luz) + ";" + str(tem) + ":"

            #enviamos datos si tenemos algun sensor
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
    
_
