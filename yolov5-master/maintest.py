import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytorch
import os
url_img = 'C:/Users/usuario/Desktop/Hexapod_Caterpie/Dataset/imagenes/1_NanoBug_Azul_17.jpg'
image = cv2.imread('C:/Users/usuario/Desktop/Hexapod_Caterpie/Dataset/imagenes/1_NanoBug_Azul_17.jpg')

height = image.shape[0]
width = image.shape[1]


def generarpuntos():
    for i in [0.132716, -0.132716]:
        for j in [0.131687, -0.131687]:
            image = cv2.circle(image, (int((0.399691+i)*width), int((0.55144+j)*height)), 2, (0,255,255), 2)

    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def train():
    # os.system(f"python train.py --img 640 --epochs 3 --data data/data.yaml --weights yolov5s.pt")
    os.system("python train.py --img 640 --batch 16 --epochs 3 --data data.yaml --weights yolov5s.pt --cache")

def test():
    for url_img in os.listdir('C:/Users/usuario/Desktop/Hexapod_Caterpie/Dataset/imagenes'):
        print(url_img)
        os.system(f'python detect.py --source {f"C:/Users/usuario/Desktop/Hexapod_Caterpie/Dataset/imagenes/{url_img}"} --data data.yaml --exist-ok --save-txt')

if __name__ == "__main__":
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    # train()
    test()