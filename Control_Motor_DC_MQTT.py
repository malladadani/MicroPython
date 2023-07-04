"""
Programa para controlar el motor mediante MQTT, su velocidad y para poder apagarlo y encenderlo
"""
import network
import time
from umqtt.simple import MQTTClient
from machine import Pin, PWM
import ssl
from time import sleep

import random
import string

orden = 0

# Configuración placa
ENB = Pin(12, Pin.OUT)
IN3 = PWM(Pin(25), freq = 100, duty = 512)
IN4 = Pin(26, Pin.OUT)

led = Pin(13, Pin.OUT)

ENB.on()
IN4.off()

# Configuración de la conexión Wifi
ssid = 'realme_8_pro'
password = 'mallada6'
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    pass


###Nombre cliente
name_client = 'mallada_'+''.join(random.choice(string.ascii_uppercase + string.digits)
                                 for x in range(0))

# Configuración de las credenciales de MQTT
mqtt_server = '156.35.154.170'
mqtt_port = 1883
mqtt_user = 'motores'
mqtt_password = '2motores3'
mqtt_topic = 'ae/motor1/ordenes'
mqtt_topic_2 = 'ae/motor1/led'

mqtt_client = MQTTClient(name_client, mqtt_server, port = mqtt_port, user = mqtt_user, password = mqtt_password, ssl = False)

while True:
    try:
        mqtt_client.connect()
    except Exception:
        continue
    break

# Conexión al broker MQTT y subscripción al tópico
time.sleep(1)
print("Conexión lograda")
print("Subscripción lograda")

def leer(topic, message):
    print((topic, message))
    global orden
    
    if(topic.decode() == "ae/motor1/led"):
        if(message.decode() == "on"):
            led.on()
            ENB.on()
        
        else:
            led.off()
            ENB.off()

    if(topic.decode() == "ae/motor1/ordenes"):
        orden = int(message)
        if(orden>100):
            orden = 100
        if(orden<0):
            orden = 0
        

        
def conversion(entrada):
    salida = entrada*10.23
    salida = int(salida)
    if (salida>1023):
        salida = 1023
    
    return salida

    
mqtt_client.set_callback(leer)
mqtt_client.subscribe(mqtt_topic)
mqtt_client.subscribe(mqtt_topic_2)

while True:
    
    mqtt_client.wait_msg()
    valor = conversion(orden)
    IN3.duty(valor)
