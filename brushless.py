from time import sleep
from machine import PWM, Pin, ADC


# Configuración de puertos

ENA = Pin(17, Pin.OUT)
Fase_U = Pin(16, Pin.OUT)

ENB = Pin(4, Pin.OUT)
Fase_V = Pin(0, Pin.OUT)

ENC = Pin(2, Pin.OUT)
Fase_W = Pin(15, Pin.OUT)

SH2 = Pin(32, Pin.IN)
SH1 = Pin(34, Pin.IN)
SH3 = Pin(35, Pin.IN)


SH3_adc = ADC(Pin(32))
SH2_adc = ADC(Pin(34))
SH1_adc = ADC(Pin(35))


boton_1 = Pin(14, Pin.IN)
# Inicialización

global estado 
estado = 1

vector_HALL = [SH1.value(), SH2.value(), SH3.value()]

Tm = 0.01

# Funcion interrupcion

def interrupcion(pin):
    global estado
    sleep(0.2)
    print("Interrupcion")
    
    estado = estado + 1


# Conf interrupcion
boton_1.irq(trigger = Pin.IRQ_RISING, handler = interrupcion)


# Cong Brushless
pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)    # Full range: 3.3 V

valor = 0

hall_A = Pin(33, Pin.IN)
hall_B = Pin(32, Pin.IN)
hall_C = Pin(35, Pin.IN)

sens_HALL = [hall_A.value(), hall_B.value(), hall_C.value()]


while True:
   
    global estado
    #global valor
    
    valor = 4090 - pot.read()
    
    if (estado == 1):
        ENA.on()
        Fase_U.on()

        ENB.on()
        Fase_V.off()

        ENC.off()
        # Condiciona a que esten abiertos ambos transistores

        estado = 2
        sleep(Tm)
        
        print(sens_HALL)
    
    if (estado == 2):
        ENA.on()
        Fase_U.on()

        ENB.off()
        # Condiciona a que esten abiertos ambos transistores
            
        ENC.on()
        Fase_W.off()

        estado = 3
        sleep(Tm)
        
        print(sens_HALL)
        
    if (estado == 3):
        ENA.off()
        # Condiciona a que esten abiertos ambos transistores

        ENB.on()
        Fase_V.on()

        ENC.on()
        Fase_W.off()

        estado = 4
        sleep(Tm)
        
        print(sens_HALL)
        
    if (estado == 4):
        ENA.on()
        Fase_U.off()

        ENB.on()
        Fase_V.on()

        ENC.off()
        # Condiciona a que esten abiertos ambos transistores

        estado = 5
        sleep(Tm)
    
        print(sens_HALL)
            
    if (estado == 5):
        ENA.on()
        Fase_U.off()

        ENB.off()
        # Condiciona a que esten abiertos ambos transistores

        ENC.on()
        Fase_W.on()

        estado = 6
        sleep(Tm)

        print(sens_HALL)

    if (estado == 6):
        ENA.off()
        # Condiciona a que esten abiertos ambos transistores

        ENB.on()
        Fase_V.off()

        ENC.on()
        Fase_W.on()

        estado = 1
        sleep(Tm)
        
        print(sens_HALL)
        
    else:
        print("Error")
    
    print(estado)

 