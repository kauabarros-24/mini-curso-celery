from fastapi import FastAPI
import time
from src.tasks import long_task, process_data_and_sending_email
from src.models import Email

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
    