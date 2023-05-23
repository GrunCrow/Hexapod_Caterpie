import os
import shutil
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

n_iteraciones = 20
umbral_de_distancia = 100
umbral_distancia_lateral = 10

posicion_inicial_cabeza = 50
posicion_inicial_cabeza_lateral = 90

giro_cabeza_lateral = 30
maximo_cabeza = 50

velocidad_atras = 10
velocidad_giro = 10
velocidad_recto = 10

# Flag de movimiento
movimiento = False
movimiento_atras = False

# Flag de cabeza girada
F_Girado = False
n_iteraciones_cabeza = 10

girar = False


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


def calibrar(c, data):
    for i in range(len(legs)):
        command = cmd.CMD_CALIBRATION + '#' + legs[i] + '#' + str(data[i][0]) + '#' + str(data[i][1]) + '#' + str(
            str(data[i][2])) + '\n'
        c.send_data(command)


def getDistance(distancias):
    distance_cm = sorted(distancias)
    return int(distance_cm[int(len(distancias) / 2)])


def stop_robot():
    stop = False
    if keyboard.is_pressed("r"):
        stop = True

    return stop


def moveHead_Horizontal(angle):
    # angle = str(180-self.slider_head_1.value())
    command = cmd.CMD_HEAD + "#" + "1" + "#" + str(angle) + '\n'

    return command


def moveHead_initialPosition():
    return cmd.CMD_HEAD + '#0#' + str(posicion_inicial_cabeza) + '\n' + cmd.CMD_HEAD + "#" + "1" + "#" + str(
        posicion_inicial_cabeza_lateral) + '\n'


def moveHead_initialPosition_lateral():
    return cmd.CMD_HEAD + "#" + "1" + "#" + str(posicion_inicial_cabeza_lateral) + '\n'


if __name__ == "__main__":

    fichero = open("./Client/point.txt")
    linea = fichero.readline()
    data = []
    while linea != '':
        data.append(linea.split('\t'))
        linea = fichero.readline()
    c = Client()
    c.turn_on_client("192.168.50.100")
    c.tcp_flag = True
    receive_instruction(c, "192.168.50.100")
    calibrar(c, data)
    videoThread = threading.Thread(target=c.receiving_video, args=("192.168.50.100",))
    videoThread.start()

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

    # command = cmd.CMD_HEAD + '#0#' + str(posicion_inicial_cabeza) + '\n'
    command = moveHead_initialPosition()
    c.send_data(command)
    time.sleep(2)
    stop = False

    if os.path.exists("Client/yolov5master/runs/detect/Puntos"):
        shutil.rmtree("Client/yolov5master/runs/detect/Puntos")
        os.makedirs("Client/yolov5master/runs/detect/Puntos")

    while not stop:
        # LEER SONAR
        distancias = []
        distancias_derecha = []
        distancias_izquierda = []

        if F_Girado:
            # Girar la cabeza a la izquierda, 3 del sonar, girar cabeza a la derecha, 3 del sonar si en alguno la distancia por debajo del umbral -> girar
            # print("Girando mi cabeza a la izquierda")
            girar_izquierda = moveHead_Horizontal(posicion_inicial_cabeza_lateral - giro_cabeza_lateral)
            c.send_data(girar_izquierda)
            time.sleep(0.5)

            for _ in range(n_iteraciones_cabeza):
                command = cmd.CMD_SONIC + '\n'
                c.send_data(command)
                time.sleep(0.3)

            time.sleep(3)

            # Volver a la posicion inicial
            command = moveHead_initialPosition()
            c.send_data(command)

            # Giro a la derecha
            # print("Girando mi cabeza a la derecha")
            girar_derecha = moveHead_Horizontal(posicion_inicial_cabeza_lateral + giro_cabeza_lateral)
            c.send_data(girar_derecha)
            time.sleep(0.3)

            time.sleep(3)

            # Volver a la posicion inicial
            command = moveHead_initialPosition()
            c.send_data(command)

            # for _ in range(n_iteraciones_cabeza):
            #     command = cmd.CMD_SONIC + '\n'
            #     c.send_data(command)
            #     time.sleep(0.3)

        # Comando Leer Sonar n_veces
        for i in range(n_iteraciones):
            command = cmd.CMD_SONIC + '\n'
            c.send_data(command)
            time.sleep(0.3)

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
                distancia = int(data[1])
                # print('Obstacle:' + str(distancia) + 'cm')
                distancias = np.append(distancias, distancia)

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

        # Si ha habido giro los n_iteraciones_cabeza primeros son de izq, luego derecha, luego recto
        if F_Girado:
            distancias_izquierda = distancias[:n_iteraciones_cabeza]
            distancias_derecha = distancias[n_iteraciones_cabeza:2 * n_iteraciones_cabeza]
            distancias = distancias[2 * n_iteraciones_cabeza:]

            # distancias_izquierda = distancias_izquierda[distancias_izquierda != 0]

            # distancias_derecha = distancias_derecha[distancias_derecha != 0]

            if distancias_izquierda.size != 0:
                valor_distancia_izquierda = int(statistics.mode(distancias_izquierda))
            else:
                valor_distancia_izquierda = 0

            if distancias_derecha.size != 0:
                valor_distancia_derecha = int(statistics.mode(distancias_derecha))
            else:
                valor_distancia_derecha = 0

            print("Mediana de las distancias izq = ", valor_distancia_izquierda)
            print("Mediana de las distancias decha = ", valor_distancia_derecha)

            if valor_distancia_izquierda > umbral_de_distancia: girar = True
            if valor_distancia_derecha > umbral_de_distancia: girar = True

            # if valor_distancia_izquierda == 0 and valor_distancia_derecha == 0 and valor_distancia == 0: girar = True

            F_Girado = False

        # distancias = distancias[distancias != 0]

        # Si la mediana es superior al umbral -> GIRAR
        # if len(distancias) == n_iteraciones:
        if distancias.size != 0:
            valor_distancia = int(statistics.mode(distancias))
        else:
            valor_distancia = 0

        print("Mediana de las distancias = ", valor_distancia)
        if valor_distancia >= umbral_de_distancia: girar = True

        if girar:
            if movimiento_atras:
                # Va para atrás
                print("Voy para atrás")

                if movimiento:
                    command = cmd.CMD_MOVE + '#1#0#-10#' + str(velocidad_atras) + '#0' + '\n'
                    c.send_data(command)

            # time.sleep(1)
            # Gira
            for j in range(1):
                print("Giro!")

                if movimiento:
                    command = cmd.CMD_MOVE + '#1#0#0#' + str(velocidad_giro) + '#10' + '\n'
                    c.send_data(command)

            F_Girado = True
            girar = False

            # time.sleep(1)
        # Si no, sigue caminando recto
        else:
            print("Camino recto")
            if movimiento:
                zancada = 5
                command = cmd.CMD_MOVE + '#1#0#' + str(zancada) + '#' + str(velocidad_recto) + '#0' + '\n'
                c.send_data(command)
                time.sleep(1)
        # FIN DEL BUCLE DE N_ITERACIONES
        print(
            "================================================================================================================================================")

        stop = stop_robot()

        '''if keyboard.is_pressed("r"):
            command = cmd.CMD_MOVE + '#0#0#0#0#0' + '\n'
            c.send_data(command)
            time.sleep(3)
            c.turn_off_client()
            break'''
    '''if c.video_flag == False:
        height, width, bytesPerComponent = c.image.shape
        # print (height, width, bytesPerComponent)
        cv2.cvtColor(c.image, cv2.COLOR_BGR2RGB, c.image)
        QImg = QImage(c.image.data.tobytes(), width, height, 3 * width, QImage.Format_RGB888)
        c.video_flag = True'''

    print("Finalizando conexion + \n")
    command = cmd.CMD_MOVE + '#0#0#0#0#0' + '\n'
    c.send_data(command)
    time.sleep(1)
    c.turn_off_client()
    print("Conexion Finalizada")
