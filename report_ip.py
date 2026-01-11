import requests
import time
import socket

# Configuración de DuckDNS
DUCKDNS_DOMAIN = "sistemaderiegoapi"  # Cambia por tu dominio en DuckDNS (sin .duckdns.org)
DUCKDNS_TOKEN = "bc3ed4ae-3296-40dd-b1e5-8284d5ace40e"  # Obtén tu token de https://www.duckdns.org

# Opcional: clave para autenticar el reporte (no usado en DuckDNS)
REPORT_KEY = None

# Obtiene la IP pública usando un servicio externo

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except Exception:
        return None

# Actualiza DuckDNS con la nueva IP

def update_duckdns(ip):
    url = f"https://www.duckdns.org/update?domains={DUCKDNS_DOMAIN}&token={DUCKDNS_TOKEN}&ip={ip}"
    try:
        res = requests.get(url, timeout=5)
        if res.text.strip() == "OK":
            print(f"DuckDNS actualizado: {DUCKDNS_DOMAIN}.duckdns.org -> {ip}")
        else:
            print("Error actualizando DuckDNS:", res.text)
    except Exception as e:
        print("Error en DuckDNS:", e)

if __name__ == "__main__":
    last_ip = None
    while True:
        ip = get_public_ip()
        if ip and ip != last_ip:
            update_duckdns(ip)
            last_ip = ip
        time.sleep(300)  # Revisa cada 5 minutos
