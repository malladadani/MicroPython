import network
import time
from umqtt.simple import MQTTClient
from machine import Pin, PWM
import ssl
from time import sleep

import random
import string

# Configuracion LED
led = Pin(23, Pin.OUT) # Patilla larga
                        # GND patilla corta
valor_led = 0

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
"""
### Abrir certificado
with open('/ca_2021_neutrino.crt','rb') as f:
    cert_data = f.read()
"""

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
    print((topic, message))
    global valor_led
    if (int(message) > 0):
        valor_led = 10
    if (int(message) <= 0):
        valor_led = -10
        
mqtt_client.set_callback(leer)

mqtt_client.subscribe(mqtt_topic)

while True:
    mqtt_client.wait_msg()
    
    if (valor_led == 10):
        while (valor_led>0):
            print(valor_led)
            valor_led = valor_led-1
        
    if (valor_led == -10):
        while (valor_led < 0):
            print(valor_led)
            valor_led = valor_led +1 

