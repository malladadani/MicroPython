import network
import time
from umqtt.simple import MQTTClient
from machine import Pin, PWM
import ssl
from time import sleep

import random
import string

# Conf motor
giro = 0
IN1 = Pin(18, Pin.OUT)
IN2 = Pin(5, Pin.OUT)
IN3 = Pin(16, Pin.OUT)
IN4 = Pin(4, Pin.OUT)
led = Pin(14, Pin.OUT)
valor = 0.02
valor_led = 0

pasos = 0

estado = 1


# Configuración de la conexión Wi-Fi
ssid = 'realme_8_pro'
password = 'mallada6'
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    pass

#### Nombre cliente
name_client = 'mallada_'+''.join(random.choice(string.ascii_uppercase + string.digits)
                                    for x in range(8))

### Abrir certificado
#with open('/ca_2021_neutrino.crt','rb') as f:
#    cert_data = f.read()



# Configuración de las credenciales de MQTT
##mqtt_server = 'neutrino.edv.uniovi.es'
mqtt_server = '156.35.154.170'

mqtt_port = 1883
mqtt_user = 'motores'
mqtt_password = '2motores3'
mqtt_topic = 'ae/motor1/ordenes'

"""
ssl_params = dict()
ssl_params["server_hostname"] = mqtt_server 
ssl_params["certfile"] = cert_data
ssl_params["cadata"] = cert_data
ssl_params["cert_reqs"] = "ssl.CERT_REQUIRED"
"""

mqtt_client = MQTTClient(name_client, mqtt_server, port=mqtt_port, user=mqtt_user, password=mqtt_password, ssl=False)


while True:
    try:
        mqtt_client.connect()
    except Exception:
        continue
    break

# Conexión al broker MQTT y suscripción al tópico
time.sleep(1)
print("Conexion lograda")

print("SUbscripcion lograda")
 
def leer(topic, message):
    global giro
    global pasos
    
    print((topic, message))
    pasos = int(message)
    print("El numero de pasos es")
    print(pasos)
    
    if (pasos > 0):
        giro == "drch"
        estado = 1
    
    if (pasos <= 0):
        giro == "izq"
        estado = 1
        
      
        
mqtt_client.set_callback(leer)

mqtt_client.subscribe(mqtt_topic)


def giro_derecha():
    global estado
    global valor
    
    if (estado == 1):
        IN1.value(1)
        IN2.value(0)
        IN3.value(0)
        IN4.value(0)
        estado = 2
        sleep(valor)
            #print(estado)

    if (estado == 2):
        IN1.value(0)
        IN2.value(0)
        IN3.value(0)
        IN4.value(1)
        estado = 3
        sleep(valor)
            #print(estado)
        
    if (estado == 3):
        IN1.value(0)
        IN2.value(1)
        IN3.value(0)
        IN4.value(0)
        estado = 4
        sleep(valor)
            #print(estado)
    
    if (estado == 4):
        IN1.value(0)
        IN2.value(0)
        IN3.value(1)
        IN4.value(0)
        estado = 1
        sleep(valor)
            #print(estado)    


def giro_izquierda():
    global estado
    global valor
    
    if (estado == 1):
        IN1.value(0)
        IN2.value(0)
        IN3.value(1)
        IN4.value(0)
        estado = 2
        sleep(valor)
            #print(estado)        
        
    if (estado == 2):
        IN1.value(0)
        IN2.value(1)
        IN3.value(0)
        IN4.value(0)
        estado = 3
        sleep(valor)
            #print(estado)

    if (estado == 3):
        IN1.value(0)
        IN2.value(0)
        IN3.value(0)
        IN4.value(1)
        estado = 4
        sleep(valor)
            #print(estado)

    if (estado == 4):
        IN1.value(1)
        IN2.value(0)
        IN3.value(0)
        IN4.value(0)
        estado = 1
        sleep(valor)
            #print(estado)

while True:
    mqtt_client.wait_msg()
    print(giro)
    
    if (giro == 'drch'):
        while (pasos > 0):
            giro_derecha()
            pasos = pasos - 1

    elif (giro == 'izq'):
        while (pasos < 0):
            giro_izquierda()
            pasos = pasos + 1
            
