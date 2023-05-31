import socket
import time

import Pyro4


numero = 2

uri = "PYRO:Robot_3@192.168.50.12:9090"
o = Pyro4.Proxy(uri)

# 0. Encender Robot

# 1. Ejecutar inicio de comunicación
print("Robot " + str(numero) + " conectando...")
o.client_connected(numero, socket.gethostname())
print("Robot " + str(numero) + " conectado")

# 2. Comenzar script movimiento del robot

numCuca = 2

# 3. Comunicar cucaracha
persecucion = o.cuca_perseguida(numero, numCuca)

time.sleep(3)

if persecucion:
    print("Persecucion valida")
elif not persecucion:
    print("Persecucion NO valida")

# 4. Close
o.libera_cuca(numero, numCuca)
# Devolver true si puede perseguirla y comenzar a perseguirla
# Devolver false si no puede, y buscar otra