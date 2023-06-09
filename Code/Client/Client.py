# -*- coding: utf-8 -*-
import io
import math
import copy
import shutil
import socket
import struct
import threading
from PID import *
from Face import *
import numpy as np
from Thread import *
import multiprocessing
from PIL import Image, ImageDraw
from Command import COMMAND as cmd
import PIL.Image as Image
import time
from yolov5master import maintest
import threading
import sys
sys.path.append("./yolov5master")
from yolov5master import maintest

from constantes import NUM_CUCAS

def bytes_to_image(image_data):
    image_file = io.BytesIO(image_data)
    image = Image.open(image_file)
    return image


def draw_red_circle(image):
    height, width, _ = image.shape
    center = (width // 2, height // 2)
    radius = 5  # Radio del círculo en píxeles
    color = (0, 0, 255)  # Color en formato BGR (rojo)
    thickness = 2  # Grosor del círculo
    image_with_circle = cv2.circle(image, center, radius, color, thickness)
    return image_with_circle


class Client:
    def __init__(self):
        self.pid=Incremental_PID(1,0,0.0025)
        self.tcp_flag=False
        self.video_flag=True
        self.fece_id=False
        self.fece_recognition_flag = False
        self.image=''
    def turn_on_client(self,ip):
        self.client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print (ip)
    def turn_off_client(self):
        try:
            self.client_socket.shutdown(2)
            self.client_socket1.shutdown(2)
            self.client_socket.close()
            self.client_socket1.close()
        except Exception as e:
            print(e)
    def is_valid_image_4_bytes(self,buf):
        bValid = True
        if buf[6:10] in (b'JFIF', b'Exif'):
            if not buf.rstrip(b'\0\r\n').endswith(b'\xff\xd9'):
                bValid = False
        else:
            try:
                Image.open(io.BytesIO(buf)).verify()
            except:
                bValid = False
        return bValid
    def receiving_video(self, ip, model, o):
        numero_robot = 2
        capturar = True

        try:
            self.client_socket.connect((ip, 8002))
            self.connection = self.client_socket.makefile('rb')
            contador = 0
        except:
            #print ("command port connect failed")
            pass
        tiempoInicio=time.time()

        if os.path.exists("Client/yolov5master/runs/detect/exp"):
            shutil.rmtree("Client/yolov5master/runs/detect/exp")
        contador=0
        while True:
            try:
                tiempoFinal = time.time()
                stream_bytes= self.connection.read(4)
                leng=struct.unpack('<L', stream_bytes[:4])
                jpg=self.connection.read(leng[0])

                if os.path.exists("Client/yolov5master/runs/detect/exp"):
                    shutil.rmtree("Client/yolov5master/runs/detect/exp")
                print("foto cogida")
                image=bytes_to_image(jpg)
                nombre_file = "salida.jpg"
                image.save(nombre_file)

                # Hace la deteccion de la img tomada
                timeRedAntes = time.time()
                maintest.test(nombre_file)
                print(time.time() - timeRedAntes)
                # image_deteccion = "Client/yolov5master/runs/detect/exp/salida.jpg"
                detect=model(image)


                print("\n\n==========================================================================================================================================================\n")

                if "(no detections)" not in str(detect):

                    str_detect = str(detect).split("\n")[0].split(" 300x400 ")[1]
                    current_detect = str_detect

                    contador_detectadas = 0
                    num_detectadas = 0
                    if "," in current_detect:
                        str_detect_array = str_detect.split(",")
                        num_detectadas = len(str_detect_array)
                        current_detect = str_detect_array[contador_detectadas]
                        contador_detectadas += 1

                    current_detect_number = current_detect.split(" ")[0]
                    current_detect = current_detect.split(" ")[1]
                    if int(current_detect_number) > 1:
                        current_detect = current_detect[:-1]

                    print(current_detect)

                    n_nanobug = NUM_CUCAS[current_detect] - 1

                    print(n_nanobug)

                    persecucion = o.cuca_perseguida(numero_robot, n_nanobug)
                    time.sleep(3)

                    while not persecucion and num_detectadas < contador_detectadas:

                        current_detect = str_detect_array[contador_detectadas]
                        contador_detectadas += 1

                        current_detect = current_detect.split(" ")[1]

                        print(current_detect)

                        n_nanobug = NUM_CUCAS[current_detect] - 1

                        print(n_nanobug)

                        persecucion = o.cuca_perseguida(numero_robot, n_nanobug)

                        time.sleep(3)

                    if persecucion:
                        print("Persecucion valida")
                        capturar = True
                        imagenRed = np.squeeze(detect.render())
                        imagenGuardar=Image.fromarray(imagenRed)
                        imagenGuardar.save(f"Cucarachas_{contador}.jpg")
                        print("Imagen guardada")
                        contador+=1
                        o.libera_cuca(numero_robot, n_nanobug)
                        time.sleep(5)
                    elif not persecucion:
                        print("Persecucion NO valida")
                        capturar = False

                    print("\n\n==========================================================================================================================================================\n")

                    # image 1 / 1: 300x400 1 2_NanoBug_Negro, 1 7_NanoBug_Naranja\n
                    # Speed: 3.0 ms pre - process, 68.0 ms inference, 5.0 ms NMS per image at shape(1, 3, 480, 640)

                    print("\n=======================================================================================================================================================\n")


                # # Leer fichero de labels
                # if os.path.isfile(r'Client\yolov5master\runs\detect\exp\labels\salida.txt'):
                #     with open(r'Client\yolov5master\runs\detect\exp\labels\salida.txt', 'r') as f:
                #         if f.read(1)!="0":
                #
                #             # Copia imagen detectada en el path de Puntos
                #             # shutil.copy(image_deteccion, f"Client/yolov5master/runs/detect/Puntos/Cucarachas_{contador}.png")
                #             #image_deteccion.save(f"Client/yolov5master/runs/detect/Puntos/Cucarachas_{contador}.png")
                #             print("DETECTA CUCARACHA ", f.read(1))
                #             contador += 1
                #
                #         elif f.read(1)=="0":
                #             print("Detecta robot")
                #     f.close()
                # else:
                #     print("No detecta nada")

                tiempoInicio=time.time()


                if self.is_valid_image_4_bytes(jpg):
                    if self.video_flag:
                        self.image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                        if self.fece_id == False and self.fece_recognition_flag:
                            self.face.face_detect(self.image)
                        #self.video_flag=False
                        self.image=draw_red_circle(self.image)
                        imagenRed=np.squeeze(detect.render())
                        cv2.imshow('VideoHexapod2',cv2.cvtColor(imagenRed,cv2.COLOR_BGR2RGB))

            except BaseException as e:
                print(e)
                break

            cv2.waitKey(1)
        cv2.destroyAllWindows()
        cv2.waitKey(0)

    def receive_instruction(self, ip):
        try:
            self.client_socket1.connect((ip, 5002))
            self.tcp_flag = True
            print("Connecttion Successful !")
        except Exception as e:
            print("Connect to server Faild!: Server IP is right? Server is opend?")
            self.tcp_flag = False
    def send_data(self,data):
        if self.tcp_flag:
            try:
                self.client_socket1.send(data.encode('utf-8'))
            except Exception as e:
                print(e)
    def receive_data(self):
        data=""
        data=self.client_socket1.recv(1024).decode('utf-8')
        return data

if __name__ == '__main__':
    c=Client()
    c.face_recognition()
