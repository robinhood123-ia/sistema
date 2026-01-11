#!/usr/bin/env python3
# Monitorea el log y controla las 12 válvulas según los logs

import RPi.GPIO as GPIO
import time
from pathlib import Path
import re

# Asignación de GPIO y pin físico para cada válvula:
# 1: GPIO17 (Pin 11), 2: GPIO18 (Pin 12), 3: GPIO27 (Pin 13), 4: GPIO22 (Pin 15)
# 5: GPIO23 (Pin 16), 6: GPIO24 (Pin 18), 7: GPIO25 (Pin 22), 8: GPIO5 (Pin 29)
# 9: GPIO6 (Pin 31), 10: GPIO12 (Pin 32), 11: GPIO13 (Pin 33), 12: GPIO19 (Pin 35)
VALVES = {
    1: 17, 2: 18, 3: 27, 4: 22, 5: 23, 6: 24,
    7: 25, 8: 5, 9: 6, 10: 12, 11: 13, 12: 19
}
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for pin in VALVES.values():
    GPIO.setup(pin, GPIO.OUT)

LOG_FILE = Path("/home/robinson/sistemafinal/logs/backend.log")

def tail_f(file_path):
    """Generador que imita 'tail -f'"""
    with open(file_path, "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line

def control_valve(line):
    # Busca logs tipo: "Válvula X ENCENDIDA" o "Válvula X APAGADA"
    match = re.search(r"Válvula (\\d+) (ENCENDIDA|APAGADA)", line)
    if match:
        valve_id = int(match.group(1))
        action = match.group(2)
        pin = VALVES.get(valve_id)
        if pin:
            if action == "ENCENDIDA":
                GPIO.output(pin, GPIO.HIGH)
                print(f"GPIO {pin} (Válvula {valve_id}) ENCENDIDA")
            elif action == "APAGADA":
                GPIO.output(pin, GPIO.LOW)
                print(f"GPIO {pin} (Válvula {valve_id}) APAGADA")

def main():
    if not LOG_FILE.exists():
        print(f"No se encontró el archivo de log: {LOG_FILE}")
        return

    print(f"Escuchando logs para {LOG_FILE} ...")
    try:
        for line in tail_f(LOG_FILE):
            control_valve(line)
    except KeyboardInterrupt:
        print("Deteniendo monitor de válvulas...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
