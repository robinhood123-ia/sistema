from fastapi import FastAPI, Header, HTTPException
from valves import turn_on, turn_off, get_status
from scheduler import schedule_valve
from logger import log
from config import API_TOKEN

app = FastAPI(title="Sistema de Riego API")

def check_token(token: str | None):
    if token != API_TOKEN:
        log("UNAUTHORIZED ACCESS ATTEMPT")
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.on_event("startup")
def startup():
    log("API STARTED")

@app.get("/status")
def status(x_api_token: str | None = Header(None)):
    check_token(x_api_token)
    log("STATUS REQUEST")
    return get_status()

@app.post("/valve/{valve_id}/on")
def valve_on(valve_id: int, x_api_token: str | None = Header(None)):
    check_token(x_api_token)
    turn_on(valve_id)
    return {"valve": valve_id, "state": "ON"}

@app.post("/valve/{valve_id}/off")
def valve_off(valve_id: int, x_api_token: str | None = Header(None)):
    check_token(x_api_token)
    turn_off(valve_id)
    return {"valve": valve_id, "state": "OFF"}

@app.post("/valve/{valve_id}/schedule")
def valve_schedule(valve_id: int, seconds: int, x_api_token: str | None = Header(None)):
    check_token(x_api_token)
    schedule_valve(valve_id, seconds)
    return {
        "valve": valve_id,
        "scheduled": True,
        "duration": seconds
    }

