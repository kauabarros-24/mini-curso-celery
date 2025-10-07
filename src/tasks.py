import time
import logging
from celery import Celery
from src.config import REDIS_URL

app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)

@app.task
def long_task():
    time.sleep(10)
    logging.Logger("Ola adadadadadada")
    
    return {"message": "Finished tasks with celery"}
    