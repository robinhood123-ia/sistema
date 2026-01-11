from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

raspberry_ip = None

class IPReport(BaseModel):
    ip: str
    key: Optional[str] = None  # Opcional: para autenticar el reporte

@app.post("/report-ip")
def report_ip(data: IPReport):
    global raspberry_ip
    raspberry_ip = data.ip
    return {"status": "ok", "ip": raspberry_ip}

@app.get("/raspberry-ip")
def get_raspberry_ip():
    if raspberry_ip:
        return {"ip": raspberry_ip}
    return {"error": "No IP reported yet"}
