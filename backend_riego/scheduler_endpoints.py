# scheduler_endpoints.py

from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from datetime import datetime, timedelta
from backend_riego.scheduler import schedule_valve_hours
from backend_riego.logger import log_event

router = APIRouter()

class ScheduleRequest(BaseModel):
    start: str
    end: str

@router.post("/valve/{valve_id}/schedule_hours")
async def valve_schedule_hours(valve_id: int, req: ScheduleRequest = Body(...)):
    """
    Programa la válvula indicada para encenderse y apagarse automáticamente
    entre las fechas y horas especificadas.
    """
    now = datetime.now()
    
    # Parsear fechas con o sin segundos
    try:
        try:
            start_dt = datetime.strptime(req.start, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            start_dt = datetime.strptime(req.start, "%Y-%m-%dT%H:%M")
        try:
            end_dt = datetime.strptime(req.end, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            end_dt = datetime.strptime(req.end, "%Y-%m-%dT%H:%M")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Formato inválido. Use YYYY-MM-DDTHH:MM o YYYY-MM-DDTHH:MM:SS"
        )

    # Validaciones
    if end_dt <= start_dt:
        raise HTTPException(status_code=400, detail="La hora de fin debe ser posterior a la hora de inicio.")
    if (end_dt - start_dt) > timedelta(days=7):
        raise HTTPException(status_code=400, detail="El rango máximo permitido es de 7 días.")
    
    log_event(f"Programando válvula {valve_id} de {start_dt} a {end_dt} (ahora: {now})")

    # Llamar al scheduler
    schedule_valve_hours(valve_id, start_dt, end_dt)

    return {
        "id": valve_id,
        "status": "scheduled_hours",
        "start": req.start,
        "end": req.end
    }
