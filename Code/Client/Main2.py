import sys
import math
import time

from ui_led import Ui_led
from ui_face import Ui_Face
from ui_client import Ui_client
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Client import *
from Calibration import *
import keyboard
import numpy as np
import statistics

legs = ["one", "two", "three", "four", "five", "six"]

n_iteraciones = 5
umbral_de_distancia = 200
posicion_inicial_cabeza = 70
maximo_cabeza = 69

velocidad_atras = 5
velocidad_giro = 4
velocidad_recto = 3

def comprobar_cabeza(posicion_cabeza):
    return posicion_cabeza <= maximo_cabeza


def receive_instruction(client, ip):
    try:
        client.client_socket1.connect((ip, 5002))
        client.tcp_flag = True
        print("Connecttion Successful !")
    except Exception as e:
        print("Connect to server Faild!: Server IP is right? Server is opend?")
        client.tcp_flag = False


def calibrar(c,data):
    for i in range(len(legs)):
        command = cmd.CMD_CALIBRATION + '#' + legs[i] + '#' + str(data[i][0]) + '#' + str(data[i][1]) + '#' + str(
            str(data[i][2])) + '\n'
        c.send_data(command)


def getDistance(distancias):
    distance_cm = sorted(distancias)
    return int(distance_cm[int(len(distancias) / 2)])

if __name__ == "__main__":

    fichero = open("point.txt")
    linea = fichero.readline()
    data = []
    while linea != '':
        data.append(linea.split('\t'))
        linea = fichero.readline()
    c = Client()
    c.turn_on_client("192.168.50.100")
    c.tcp_flag = True
    receive_instruction(c, "192.168.50.100")
    calibrar(c,data)

    """
    AYUDA MOVIMIENTO
    command = cmd.CMD_MOVE + "#" + str(self.gait_flag) + "#" + str(round(x)) + "#" + str(round(y)) \
              + "#" + str(speed) + "#" + str(round(angle)) + '\n'
    MOVERSE
    command=cmd.CMD_MOVE+'#1#0#35#0#10#0'+'\n'
    c.send_data(command)
    """



    command = cmd.CMD_BUZZER + '#1' + '\n'
    c.send_data(command)
    time.sleep(1)
    command = cmd.CMD_BUZZER + '#0' + '\n'
    c.send_data(command)
    command = cmd.CMD_SERVOPOWER + "#" + "1" + '\n'
    c.send_data(command)
    time.sleep(2)
    command = cmd.CMD_BALANCE + '#1' + '\n'
    c.send_data(command)
    time.sleep(2)

    # Inclinar la cabeza a la posición inicial

    '''command = cmd.CMD_HEAD + '#0#' + str(posicion_inicial_cabeza) + '\n'
    c.send_data(command)
    time.sleep(2)'''

    '''while True:
                            #LEER SONAR

        distancias = []
        for i in range(n_iteraciones):
            # Comando Leer Sonar (único comando)
            command = cmd.CMD_SONIC + '\n'
            c.send_data(command)
            time.sleep(0.5)

            # Intenta recibir los datos
            try:
                alldata = c.receive_data()
            except:
                c.tcp_flag = False
                break
            # print(alldata)

            # Si no recibe nada
            if alldata == '':
                break
            # Si recibe está separado por saltos de linea, hacer array en el que cada elemento sea el dato
            else:
                cmdArray = alldata.split('\n')
                # print(cmdArray)
                if cmdArray[-1] != "":
                    cmdArray == cmdArray[:-1]

            # Numero de comandos
            # print(len(cmdArray))

            # Por cada comando del CMDArray
            for oneCmd in cmdArray:
                data = oneCmd.split("#")
                # print(data)

                # Si Comando vacío
                if data == "":
                    c.tcp_flag = False
                    break

                # Si el comando es CMD_SONIC -> Mostrar distancia detectada
                elif data[0] == cmd.CMD_SONIC:
                    # print('Obstacle:' + str(data[1]) + 'cm')
                    distancias=np.append(distancias,int(data[1]))

                # Si el comando es CMD_POWER -> muestra la batería
                elif data[0] == cmd.CMD_POWER:
                    try:
                        power_value = []
                        if len(data) == 3:
                            power_value[0] = data[1]
                            power_value[1] = data[2]
                            # self.power_value[0] = self.restriction(round((float(data[1]) - 5.00) / 3.40 * 100),0,100)
                            # self.power_value[1] = self.restriction(round((float(data[2]) - 7.00) / 1.40 * 100),0,100)
                            print('Power：', power_value[0], power_value[1])
                    except Exception as e:
                        print(e)

            # Si la mediana es superior al umbral -> GIRAR
            if len(distancias) == n_iteraciones:
                if int(statistics.mode(distancias)) >= umbral_de_distancia:
                    print(distancias)
                    print("Mediana de las distancias = ", statistics.mode(distancias))
                    # Va para atrás
                    print("Voy para atrás")
                    command = cmd.CMD_MOVE + '#1#0#-10#' + str(velocidad_atras) + '#0' + '\n'
                    c.send_data(command)
                    time.sleep(3)
                    # Gira
                    for j in range(5):
                        print("Giro!")
                        command = cmd.CMD_MOVE + '#1#0#0#' + str(velocidad_giro) + '#10' + '\n'
                        c.send_data(command)
                        time.sleep(3)
                    # Si no, sigue caminando recto
                else:
                    print("Camino recto")
                    command = cmd.CMD_MOVE + '#1#0#35#' + str(velocidad_recto) + '#0' + '\n'
                    c.send_data(command)
                    time.sleep(3)
            # FIN DEL BUCLE DE N_ITERACIONES

        if keyboard.is_pressed("r"):
            command = cmd.CMD_MOVE + '#0#0#0#0#0' + '\n'
            c.send_data(command)
            time.sleep(3)
            break'''

    for i in range(3):
        command = cmd.CMD_MOVE + '#1#0#35#10#0' + '\n'
        c.send_data(command)
        time.sleep(5)

    for i in range(3):
        command = cmd.CMD_MOVE + '#1#35#0#10#0' + '\n'
        c.send_data(command)
        time.sleep(5)

    for i in range(3):
        command = cmd.CMD_MOVE + '#2#0#-35#10#10' + '\n'
        c.send_data(command)
        time.sleep(5)
    for i in range(3):
        command = cmd.CMD_MOVE + '#2#35#0#10#10' + '\n'
        c.send_data(command)
        time.sleep(5)
