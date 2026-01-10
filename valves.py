import json
from logger import log
from config import TOTAL_VALVES, STATE_FILE

# ESTADO EN MEMORIA
valve_state = {i: False for i in range(1, TOTAL_VALVES + 1)}

# CARGAR ESTADO EXISTENTE
def load_state():
    global valve_state
    try:
        with open(STATE_FILE, "r") as f:
            valve_state = json.load(f)
            # convertir claves a int
            valve_state = {int(k): v for k, v in valve_state.items()}
        log("STATE LOADED")
    except FileNotFoundError:
        log("STATE FILE NOT FOUND, USING DEFAULT")
    except Exception as e:
        log(f"ERROR LOADING STATE: {e}")

# GUARDAR ESTADO
def save_state():
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(valve_state, f)
        log("STATE SAVED")
    except Exception as e:
        log(f"ERROR SAVING STATE: {e}")

def turn_on(valve_id: int):
    valve_state[valve_id] = True
    log(f"VALVE {valve_id} -> ON")
    save_state()

def turn_off(valve_id: int):
    valve_state[valve_id] = False
    log(f"VALVE {valve_id} -> OFF")
    save_state()

def get_status():
    return valve_state

# cargar estado al inicio
load_state()
