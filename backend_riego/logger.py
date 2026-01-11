import datetime
import os

LOG_FILE = "/home/robinson/sistemafinal/logs/backend.log"

def log_event(message: str):
    """Imprime en consola y guarda en archivo de log."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)

    # Guardar en archivo de log
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(log_message + "\n")
    except Exception as e:
        print(f"Error escribiendo en log: {e}")
