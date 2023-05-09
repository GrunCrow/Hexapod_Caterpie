# -*- coding: utf-8 -*-
import io
import math
import copy
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

def bytes_to_image(image_data):
    image_file = io.BytesIO(image_data)
    image = Image.open(image_file)
    return image

class Client:
    def __init__(self):
        self.face=Face()
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
        while True:

            try:
                tiempoFinal = time.time()
                stream_bytes= self.connection.read(4)
                leng=struct.unpack('<L', stream_bytes[:4])
                jpg=self.connection.read(leng[0])
                if tiempoFinal-tiempoInicio>5:
                    print("foto cogida")
                    image=bytes_to_image(jpg)
                    image.save("salida.jpg")
                    tiempoInicio=time.time()
                if self.is_valid_image_4_bytes(jpg):
                    if self.video_flag:
                        self.image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                        if self.fece_id == False and self.fece_recognition_flag:
                            self.face.face_detect(self.image)
                        #self.video_flag=False
                        cv2.imshow('Video',self.image)


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
