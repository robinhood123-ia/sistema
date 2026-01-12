# scheduler.py
import threading
import time as t
from datetime import datetime
from backend_riego.valves import turn_on, turn_off
from backend_riego.logger import log_event

# Diccionarios para almacenar tareas activas
scheduled_tasks = {}
scheduled_hour_tasks = {}

# --- Programación por segundos (legacy) ---
def schedule_valve(valve_id: int, seconds: int):
    """Programa la válvula para encender por X segundos"""
    def task():
        log_event(f"[Segundos] Válvula {valve_id} ENCENDIDA por {seconds} segundos")
        turn_on(valve_id)
        t.sleep(seconds)
        turn_off(valve_id)
        log_event(f"[Segundos] Válvula {valve_id} APAGADA")
        # Eliminar tarea al finalizar
        scheduled_tasks.pop(valve_id, None)

    if valve_id in scheduled_tasks:
        log_event(f"[Segundos] Cancelando tarea previa de la válvula {valve_id}")
        scheduled_tasks[valve_id].cancel()

    thread = threading.Thread(target=task)
    thread.start()
    scheduled_tasks[valve_id] = thread

# --- Programación por horas ---

def schedule_valve_hours(valve_id: int, start: datetime, end: datetime):
    """
    Programa la válvula para encender automáticamente solo entre la fecha y hora de inicio y fin exactas.
    Funciona en background usando un thread que espera hasta la hora de inicio y luego controla la válvula.
    """
    def hour_task():
        now = datetime.now()
        log_event(f"[Fecha/Hora] Programando válvula {valve_id}: {start} -> {end} (ahora: {now})")

        # Si la hora de inicio es futura, esperar hasta entonces
        if start > now:
            wait_seconds = (start - now).total_seconds()
            log_event(f"[Fecha/Hora] Esperando {wait_seconds:.0f} segundos hasta el inicio")
            t.sleep(wait_seconds)

        # Verificar nuevamente después de esperar
        now = datetime.now()
        log_event(f"[Fecha/Hora] Después de esperar, ahora: {now}, start: {start}, end: {end}")
        if start <= now <= end:
            log_event(f"[Fecha/Hora] Válvula {valve_id} ENCENDIDA (inicio del rango)")
            turn_on(valve_id)

            # Calcular cuánto tiempo mantener encendida
            remaining_seconds = (end - now).total_seconds()
            log_event(f"[Fecha/Hora] Tiempo restante: {remaining_seconds:.0f} segundos")
            if remaining_seconds > 0:
                log_event(f"[Fecha/Hora] Manteniendo encendida por {remaining_seconds:.0f} segundos")
                t.sleep(remaining_seconds)

            # Apagar al final del rango
            log_event(f"[Fecha/Hora] Válvula {valve_id} APAGADA (fin del rango)")
            turn_off(valve_id)
        else:
            log_event(f"[Fecha/Hora] Rango de tiempo expirado o inválido para válvula {valve_id}: start <= now <= end? {start <= now <= end}, now > end? {now > end}")

    # Cancelar tarea previa si existe
    if valve_id in scheduled_hour_tasks:
        log_event(f"[Fecha/Hora] Cancelando tarea previa de la válvula {valve_id}")
        # No podemos cancelar threads daemon fácilmente, pero podemos marcar como None
        scheduled_hour_tasks[valve_id] = None

    thread = threading.Thread(target=hour_task, daemon=True)
    thread.start()
    scheduled_hour_tasks[valve_id] = thread
    log_event(f"[Fecha/Hora] Thread iniciado para válvula {valve_id}")
