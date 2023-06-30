### Librerias
from machine import ADC, Pin, PWM
    # De la libreria machine importamos los modulos ADC, Pin y PWM
from time import sleep

### Configuracion de pines
IN1 = PWM(Pin(33),freq = 200,duty=0)
IN2 = PWM(Pin(12),freq = 200,duty=0)
    # Salidas PWM para el control de los sentidos

### Configuracion potenciometro
adc15 = ADC(Pin(15))
adc15.atten(ADC.ATTN_11DB)
adc15.width(ADC.WIDTH_12BIT)
    # En este caso dispone de un potenciometro para la lectura del valor de duty, para ello configuramos el puerto 15, como entrada de la lectura del conversor con un ancho de 12 bit

############# Condiciones inciales ##############
num_estado = 0
    # Variable interna de estado

###### interrupcion #########################################333
def handle_interrupt(pin):
    global num_estado
    global valor
    sleep(0.02)
        # Antirebote
    if (num_estado == 0):
        num_estado = 1
    
    if (num_estado == 1):
        for i in range(valor,0,-1):
             IN1.duty(i)
             sleep(0.01)
        # Parada suave, en caso de que estuviese arrancado
        
        IN1.duty(0)
        sleep(0.5)
            
        for i in range(0,valor,1):
            IN2.duty(i)
            sleep(0.01)
        # Arranque suave
        
    if (num_estado == 2):
        for i in range(valor,0,-1):
            IN2.duty(i)
            sleep(0.01)
        # Parada suave, en caso de que estuviese arrancado
        
        IN2.duty(0)
        sleep(0.5)
        
        for i in range(0,valor,1):
            IN1.duty(i)
            sleep(0.01)
        # Arranque suave
        
    num_estado = num_estado + 1
        # Cambiamos de estado
    
    print("Estamos en el estado"+str(num_estado))
    
    if (num_estado > 2):
        num_estado = 1
        # Aseguramos de que no cambiamos de estado
        
def paro_interrupt(pin_paro):
    global num_estado = 0
        # Pulsador de paro

### Configuracion interrupcion
pin = Pin(14,Pin.IN,Pin.PULL_UP)
    # Se configura el pin 14 como entrada
irq = Pin.IRQ_FALLING
    # La interrupcion saltara con un flanco de subida o de bajada
pin.irq(trigger = irq, handler=handle_interrupt)
    # La funcion interrupcion sera llamada "handle_interrupt"


pin_paro = Pin(17,Pin.IN,Pin.PULL_UP)
    # Se configura el pin 17 como entrada
pin_paro.irq(trigger = irq, handler=paro_interrupcion)
    # La funcion interrupcion sera llamada "paro_interrupcion"


########### Bucle infinito ###########################
while True:
    valor = int(adc15.read()/4)
        # Leemos un valor de 0 a 1023
        
    if (num_estado == 1):
        IN1.duty(valor)
        IN2.duty(0)
        
    if (num_estado == 2):
        IN1.duty(0)
        IN2.duty(valor)
        
    if (num_estado == 0):
        IN1.duty(0)
        IN2.duty(0)
        
    sleep(0.2)
