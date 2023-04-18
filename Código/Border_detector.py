# Border detector

import time

from Code.Server import Ultrasonic


def medir_distancia(n_iteraciones=10):
    Ultrasonic.Ultrasonic.getDistance(n_iteraciones=n_iteraciones)  # en cm

    return distancia


'''def avanzar(distancia_objetivo, inclinacion_cabeza):
    # Medir la distancia actual
    distancia_actual = medir_distancia()

    # Ajustar la posición de las patas
    if distancia_actual < distancia_objetivo:
        # Mover las patas hacia adelante
        angulo_patas = 10 + inclinacion_cabeza
    elif distancia_actual > distancia_objetivo:
        # Mover las patas hacia atrás
        angulo_patas = 170 + inclinacion_cabeza
    else:
        # Mantener la posición actual de las patas
        angulo_patas = 90 + inclinacion_cabeza'''

while True:
    distancia = medir_distancia()
    print("Distancia: {:.2f} cm".format(distancia))
    time.sleep(0.1)
