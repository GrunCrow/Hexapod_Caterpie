from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import torch
import torchvision.datasets
from torchvision import datasets, transforms

import os
# url_img = 'C:/Users/usuario/Desktop/Hexapod_Caterpie/Dataset/imagenes/1_NanoBug_Azul/1_NanoBug_Azul_17.jpg'
# image = cv2.imread('C:/Users/usuario/Desktop/Hexapod_Caterpie/Dataset/imagenes/1_NanoBug_Azul/1_NanoBug_Azul_17.jpg')
#
# height = image.shape[0]
# width = image.shape[1]


# def generarpuntos():
#     for i in [0.132716, -0.132716]:
#         for j in [0.131687, -0.131687]:
#             image = cv2.circle(image, (int((0.399691+i)*width), int((0.55144+j)*height)), 2, (0, 255, 255), 2)
#
#     cv2.imshow("Image", image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

def train():
    # os.system(f"python train.py --img 640 --epochs 3 --data data/data.yaml --weights yolov5s.pt")
    # os.system("python train.py --data data/data.yaml --epochs 3 --weights '' --cfg yolov5s.yaml  --batch-size -1")
    os.system("python train.py --img 640 --batch -1 --epochs 20 --data data/data.yaml --cfg yolov5s.yaml --optimizer Adam")

def test(ruta):
    # for url_img in os.listdir('/Code/Client/yolov5master/data/test/images'):
    ruta_acceder = ruta
    print(ruta, os.path.abspath(ruta_acceder))
    os.system(f'python Client/yolov5master/detect.py --weights Client/yolov5master/runs/train/exp11/weights/best.pt --source {ruta_acceder} --data data.yaml --exist-ok --save-txt')

if __name__ == "__main__":
    #train()
    #test(r"C:\Users\usuario\Documents\GitHub\Hexapod_Caterpie\Code\Client\yolov5master\data\test\images\0_Hexapod_266_jpg.rf.9168c337923922fce12abf7cec2a0aa2.jpg")
    print()
