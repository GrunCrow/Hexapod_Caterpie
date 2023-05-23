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

def bytes_to_image(image_data):
    image_file = io.BytesIO(image_data)
    image = Image.open(image_file)
    return image

def draw_red_square(image):
    height, width, _ = image.shape
    center_x, center_y = width // 2, height // 2
    square_size = 20  # Tamaño del cuadrado en píxeles
    half_size = square_size // 2
    top_left = (center_x - half_size, center_y - half_size)
    bottom_right = (center_x + half_size, center_y + half_size)
    color = (0, 0, 255)  # Color en formato BGR (rojo)
    thickness = 2  # Grosor del cuadrado
    image_with_square = cv2.rectangle(image, top_left, bottom_right, color, thickness)
    return image_with_square


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
    def receiving_video(self,ip):
        try:
            self.client_socket.connect((ip, 8002))
            self.connection = self.client_socket.makefile('rb')
            contador=0
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
                if tiempoFinal-tiempoInicio>5:
                    if os.path.exists("Client/yolov5master/runs/detect/exp"):
                        shutil.rmtree("Client/yolov5master/runs/detect/exp")
                    print("foto cogida")
                    image=bytes_to_image(jpg)
                    nombre_file = "salida.jpg"
                    image.save(nombre_file)
                    maintest.test(nombre_file)
                    # Leer fichero de labels
                    if os.path.isfile(r"Client\yolov5mater\runs\detect\exp\labels\salida.txt'"):
                        with open(r'Client\yolov5master\runs\detect\exp\labels\salida.txt', 'r') as f:
                            if f.read(1)!="0":
                                image.save(f"Client/yolov5master/runs/detect/Puntos/Cucarachas_{contador}")
                                print("DETECTA CUCARACHA ",f.read(1))
                                contador += 1
                            elif f.read(1)=="0":
                                print("Detecta robot")
                            else:
                                print("No detecta nada")
                        f.close()
                    tiempoInicio=time.time()


                if self.is_valid_image_4_bytes(jpg):
                    if self.video_flag:
                        self.image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                        if self.fece_id == False and self.fece_recognition_flag:
                            self.face.face_detect(self.image)
                        #self.video_flag=False
                        self.image=draw_red_square(self.image)
                        cv2.imshow('VideoHexapod2',self.image)

            except BaseException as e:
                print (e)
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
