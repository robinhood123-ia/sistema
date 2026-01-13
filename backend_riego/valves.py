from gpiozero import LED
from backend_riego.logger import log_event

# Asignación de pines para cada válvula (LED de prueba o relés)
# Cambia los pines si tus dispositivos usan otros GPIO
VALVES = {
    1: LED(17),  # Pin físico 11
    2: LED(18),  # Pin físico 12
    3: LED(27),  # Pin físico 13
    4: LED(22),  # Pin físico 15
    5: LED(23),  # Pin físico 16
    6: LED(24),  # Pin físico 18
    7: LED(25),  # Pin físico 22
    8: LED(5),   # Pin físico 29
    9: LED(6),   # Pin físico 31
    10: LED(12), # Pin físico 32
    11: LED(13), # Pin físico 33
    12: LED(19)  # Pin físico 35
}

# Estado interno de cada válvula (0 = apagada, 1 = encendida)
valve_states = {valve_id: 0 for valve_id in VALVES.keys()}

def turn_on(valve_id: int):
    """Enciende la válvula/LED"""
    if valve_id in VALVES:
        VALVES[valve_id].on()
        valve_states[valve_id] = 1
        log_event(f"Válvula {valve_id} ENCENDIDA")
    else:
        log_event(f"Válvula {valve_id} no encontrada")

def turn_off(valve_id: int):
    """Apaga la válvula/LED"""
    if valve_id in VALVES:
        VALVES[valve_id].off()
        valve_states[valve_id] = 0
        log_event(f"Válvula {valve_id} APAGADA")
    else:
        log_event(f"Válvula {valve_id} no encontrada")

def get_status():
    """Devuelve el estado de todas las válvulas"""
    return valve_states.copy()
