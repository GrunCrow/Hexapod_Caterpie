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


def receive_instruction(client,ip):
    try:
        client.client_socket1.connect((ip, 5002))
        client.tcp_flag = True
        print("Connecttion Successful !")
    except Exception as e:
        print("Connect to server Faild!: Server IP is right? Server is opend?")
        client.tcp_flag = False

if __name__ == "__main__":

    fichero=open("point.txt")
    linea=fichero.readline()
    data=[]
    while linea!='':
        data.append(linea.split('\t'))
        linea = fichero.readline()
    #LEER DATOS PARA CALIBRACION
    one_x=str(data[0][0])
    one_y=str(data[0][1])
    one_z=str(data[0][2])
    two_x=str(data[1][0])
    two_y=str(data[1][1])
    two_z=str(data[1][2])
    three_x=str(data[2][0])
    three_y=str(data[2][1])
    three_z=str(data[2][2])
    four_x=str(data[3][0])
    four_y=str(data[3][1])
    four_z=str(data[3][2])
    five_x=str(data[4][0])
    five_y=str(data[4][1])
    five_z=str(data[4][2])
    six_x=str(data[5][0])
    six_y=str(data[5][1])
    six_z=str(data[5][2])
    c = Client()
    c.turn_on_client("192.168.50.100")
    c.tcp_flag = True
    receive_instruction(c, "192.168.50.100")
    """
    AYUDA MOVIMIENTO
    command = cmd.CMD_MOVE + "#" + str(self.gait_flag) + "#" + str(round(x)) + "#" + str(round(y)) \
              + "#" + str(speed) + "#" + str(round(angle)) + '\n'
    """
    """
    MOVERSE
    command=cmd.CMD_MOVE+'#1#0#35#0#10#0'+'\n'
    c.send_data(command)
    """

    distancias=np.array([])


    command=cmd.CMD_BUZZER+'#1'+'\n'
    c.send_data(command)
    time.sleep(1)
    command = cmd.CMD_BUZZER + '#0' + '\n'
    c.send_data(command)

    c.video_flag=False
    command = cmd.CMD_CALIBRATION + '\n'
    c.send_data(command)

    command = cmd.CMD_SERVOPOWER + "#" + "1" + '\n'
    c.send_data(command)
    time.sleep(2)
    command = cmd.CMD_BALANCE + '#1' + '\n'
    c.send_data(command)
    time.sleep(2)
    for i in range(10):
        """
        command = cmd.CMD_MOVE + '#1#0#35#10#0' + '\n'
        c.send_data(command)
        """
        # LEER SONAR
        command = cmd.CMD_SONIC + '\n'
        c.send_data(command)
        time.sleep(0.25)
        try:
            alldata = c.receive_data()
        except:
            c.tcp_flag = False
            break
        # print(alldata)
        if alldata == '':
            break
        else:
            cmdArray = alldata.split('\n')
            # print(cmdArray)
            if cmdArray[-1] != "":
                cmdArray == cmdArray[:-1]
        for oneCmd in cmdArray:
            data = oneCmd.split("#")
            print(data)
            if data == "":
                c.tcp_flag = False
                break
            elif data[0] == cmd.CMD_SONIC:
                print('Obstacle:' + data[1] + 'cm')
                distancias=np.append(distancias,data[1])
            elif data[0] == cmd.CMD_POWER:
                try:
                    power_value=[]
                    if len(data) == 3:
                        power_value[0] = data[1]
                        power_value[1] = data[2]
                        # self.power_value[0] = self.restriction(round((float(data[1]) - 5.00) / 3.40 * 100),0,100)
                        # self.power_value[1] = self.restriction(round((float(data[2]) - 7.00) / 1.40 * 100),0,100)
                        print('Power：',power_value[0],power_value[1])
                except Exception as e:
                    print(e)

        if keyboard.is_pressed("r") or i==9:
            command = cmd.CMD_SERVOPOWER + "#" + "0" + '\n'
            c.send_data(command)
            print(statistics.mode(distancias))
            c.turn_off_client()
            c.tcp_flag=False
            break

