import requests
import time
import socket

# Cambia esta URL por la del servidor central donde está el endpoint
SERVER_URL = "http://<CENTRAL_SERVER_IP>:8000/report-ip"

# Opcional: clave para autenticar el reporte
REPORT_KEY = None

# Obtiene la IP pública usando un servicio externo

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except Exception:
        return None

# Reporta la IP al servidor central

def report_ip(ip):
    data = {"ip": ip}
    if REPORT_KEY:
        data["key"] = REPORT_KEY
    try:
        res = requests.post(SERVER_URL, json=data, timeout=5)
        print("Reporte IP:", res.json())
    except Exception as e:
        print("Error reportando IP:", e)

if __name__ == "__main__":
    last_ip = None
    while True:
        ip = get_public_ip()
        if ip and ip != last_ip:
            report_ip(ip)
            last_ip = ip
        time.sleep(300)  # Revisa cada 5 minutos
