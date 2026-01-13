# scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime
import os
import logging

# Importar funciones de control de válvulas
from backend_riego.valves import turn_on, turn_off

# =========================
# LOGGER
# =========================
logger = logging.getLogger("scheduler")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

# =========================
# JOBSTORE (persistencia)
# =========================
DB_PATH = os.path.expanduser("~/riego-api/jobs.sqlite")
jobstores = {
    'default': SQLAlchemyJobStore(url=f"sqlite:///{DB_PATH}")
}

# =========================
# SCHEDULER
# =========================
scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()
logger.info("Scheduler iniciado con persistencia en %s", DB_PATH)

# =========================
# FUNCIONES DE PROGRAMACIÓN
# =========================
def schedule_valve(valve_id: int, seconds: int):
    """Programa una válvula por segundos"""
    now = datetime.now()
    end_time = now + timedelta(seconds=seconds)
    scheduler.add_job(turn_on, 'date', run_date=now, args=[valve_id])
    scheduler.add_job(turn_off, 'date', run_date=end_time, args=[valve_id])
    logger.info("Válvula %d programada por %d segundos (%s -> %s)", valve_id, seconds, now, end_time)

def schedule_valve_hours(valve_id: int, start_dt: datetime, end_dt: datetime):
    """Programa una válvula para encenderse y apagarse entre start_dt y end_dt"""
    logger.info("Programando válvula %d: %s -> %s", valve_id, start_dt, end_dt)
    
    # Job para encender la válvula
    scheduler.add_job(turn_on, 'date', run_date=start_dt, args=[valve_id], id=f"valve{valve_id}_on_{start_dt.timestamp()}")
    
    # Job para apagar la válvula
    scheduler.add_job(turn_off, 'date', run_date=end_dt, args=[valve_id], id=f"valve{valve_id}_off_{end_dt.timestamp()}")
    
    logger.info("Válvula %d programada en scheduler (on: %s, off: %s)", valve_id, start_dt, end_dt)

# =========================
# OPCIONAL: Restaurar tareas al iniciar (si quieres auto-recovery)
# =========================
def restore_jobs():
    jobs = scheduler.get_jobs()
    logger.info("Jobs restaurados al iniciar: %d", len(jobs))
    for job in jobs:
        logger.info("Job activo: %s -> %s", job.id, job.next_run_time)
