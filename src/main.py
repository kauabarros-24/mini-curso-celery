from fastapi import FastAPI
import time
from src.tasks import (
    long_task, 
    process_data_and_sending_email, 
    long_task_with_progress, 
    celery_app 
)
from src.models import Email
from celery.result import AsyncResult   

app = FastAPI()

@app.get("/api/sync-process")
def sync_process():
    time.sleep(10)
    
    return {"message": "Running sync process"}

@app.get("/api/async-process")
def async_process():
    task = long_task.delay()
    return {
        "task_id": task.id,
        "message": "Task enviada para processamento"
    }
    

@app.post("/api/send-email")
def async_mail(email: Email):
    new_email = process_data_and_sending_email.delay(to_email=email.to_email, subject=email.subject, body=email.body)
    
    return {
        "task_id": new_email.id,
        "message": "Processing send email"
    }
    
@app.post("/process-data-with-status/")
def process_data_with_status(time: int = 100):
    task = long_task_with_progress.delay(time)
    return {"message": "Processamento iniciado", "task_id": task.id}


@app.get("/task-status/{task_id}")
def task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    if result.state == "PENDING":
        return {"state": result.state, "progress": 0}
    if result.state == "PROGRESS":
        return {"state": result.state, "progress": result.info}
    if result.state == "SUCCESS":
        return {"state": result.state, "result": result.result}
    return {"state": result.state, "info": str(result.info)}