import RPi.GPIO as GPIO
from backend_riego.logger import log_event

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Asignación de GPIO y pin físico para cada válvula:
# 1: GPIO17 (Pin 11), 2: GPIO18 (Pin 12), 3: GPIO27 (Pin 13), 4: GPIO22 (Pin 15)
# 5: GPIO23 (Pin 16), 6: GPIO24 (Pin 18), 7: GPIO25 (Pin 22), 8: GPIO5 (Pin 29)
# 9: GPIO6 (Pin 31), 10: GPIO12 (Pin 32), 11: GPIO13 (Pin 33), 12: GPIO19 (Pin 35)
VALVES = {
    1: 17,  # Pin físico 11
    2: 18,  # Pin físico 12
    3: 27,  # Pin físico 13
    4: 22,  # Pin físico 15
    5: 23,  # Pin físico 16
    6: 24,  # Pin físico 18
    7: 25,  # Pin físico 22
    8: 5,   # Pin físico 29
    9: 6,   # Pin físico 31
    10: 12, # Pin físico 32
    11: 13, # Pin físico 33
    12: 19  # Pin físico 35
}

# Inicializar pines
for pin in VALVES.values():
    GPIO.setup(pin, GPIO.OUT)

def turn_on(valve_id: int):
    pin = VALVES[valve_id]
    GPIO.output(pin, GPIO.HIGH)
    log_event(f"Válvula {valve_id} ENCENDIDA")

def turn_off(valve_id: int):
    pin = VALVES[valve_id]
    GPIO.output(pin, GPIO.LOW)
    log_event(f"Válvula {valve_id} APAGADA")

def get_status():
    status = {}
    for valve_id, pin in VALVES.items():
        status[valve_id] = GPIO.input(pin)
    return status
