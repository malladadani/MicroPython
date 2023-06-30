from machine import Pin, ADC, PWM
from time import sleep
################## Configuracion Pines ###################
IN1 = Pin(14, Pin.OUT)
IN2 = Pin(27, Pin.OUT)
IN3 = Pin(26, Pin.OUT)
IN4 = Pin(25, Pin.OUT)
# Salida para los puertos del motor paso a paso

################## Configuracion ADC #####################

Pot = ADC(Pin(15))
Pot.atten(ADC.ATTN_11DB)
# Configuracion del potenciometro

################## Funcion Interrupcion ##################

# Funcion interrupcion
def handle_interrupcion(pin):
    sleep(0.02)
    global giro
    global estado
    
    estado = 0

    # Giro = 1 --> Giro horario
    # Giro = 2 --> Giro antihorario
    
    if (giro == 1):
        giro = 2
        print("Giro a 2")
        
    else:
        giro = 1
        print("Giro a 1")

    # Plantemos la posibilidad de giro horario y antihorario, esto quedara marcado por la variable "giro" 

### Configuracion interrupcion
pin = Pin(4,Pin.IN,Pin.PULL_UP)
    # Se configura el pin 14 como entrada
irq = Pin.IRQ_FALLING
    # La interrupcion saltara con un flanco de bajada
pin.irq(trigger = irq, handler=handle_interrupcion)
    # La funcion interrupcion sera llamada "handle_interrupcion"


################## Variables Estado ######################

estado = 1
    # Marca el paso de la secuencia
valor = 0
    # variable interna para guarda el valor de la lectura del conversor
giro = 1
    # Variable de giro del motor
     
################## Bucle infinito ########################

while True:
    
    valor = Pot.read()
    valor = (valor*(10**(-6)))
        # Leemos el valor del potenciometro
    
    if (valor < 1.0235*(10**-4)):
        estado = 0
        
    else:
        if (giro == 1):
            estado = 1
            if (estado == 1):
                IN1.value(1)
                IN2.value(0)
                IN3.value(0)
                IN4.value(0)
                estado = 2
                sleep(valor)

            if (estado == 2):
                IN1.value(0)
                IN2.value(0)
                IN3.value(1)
                IN4.value(0)
                estado = 3
                sleep(valor)
        
            if (estado == 3):
                IN1.value(0)
                IN2.value(1)
                IN3.value(0)
                IN4.value(0)
                estado = 4
                sleep(valor)

            if (estado == 4):
                IN1.value(0)
                IN2.value(0)
                IN3.value(0)
                IN4.value(1)
                estado = 1
                sleep(valor)
        
        if (giro == 2):
            estado = 1
            if (estado == 1):
                IN1.value(0)
                IN2.value(0)
                IN3.value(0)
                IN4.value(1)
                estado = 2
                sleep(valor)

            if (estado == 2):
                IN1.value(0)
                IN2.value(1)
                IN3.value(0)
                IN4.value(0)
                estado = 3
                sleep(valor)
        
            if (estado == 3):
                IN1.value(0)
                IN2.value(0)
                IN3.value(1)
                IN4.value(0)
                estado = 4
                sleep(valor)

            if (estado == 4):
                IN1.value(1)
                IN2.value(0)
                IN3.value(0)
                IN4.value(0)
                estado = 1
                sleep(valor)
