from fastapi import FastAPI
import time
from src.tasks import long_task

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