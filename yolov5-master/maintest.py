import cv2
import numpy as np
import matplotlib.pyplot as plt
image = cv2.imread('C:/Users/usuario/Desktop/Hexapod_Caterpie/Dataset/imagenes/1_NanoBug_Azul_17.jpg')
height = image.shape[0]
width = image.shape[1]

for i in [0.132716, -0.132716]:
    for j in [0.131687, -0.131687]:
        image = cv2.circle(image, (int((0.399691+i)*width), int((0.55144+j)*height)), 2, (0,255,255), 2)

cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()