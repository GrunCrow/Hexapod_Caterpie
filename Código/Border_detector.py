# Border detector

import RPi.GPIO as GPIO
import time

# Configurar los pines GPIO para el sensor de sonar
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)


def medir_distancia():
    # Enviar un pulso al sensor de sonar
    GPIO.output(TRIGGER_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, GPIO.LOW)

    # Medir el tiempo que tarda el sonido en reflejarse
    t_inicio = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        t_inicio = time.time()
    t_fin = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        t_fin = time.time()

    # Calcular la distancia en centímetros
    duracion = t_fin - t_inicio
    distancia = duracion * 34300 / 2
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