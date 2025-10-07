from fastapi import FastAPI
import time
import logging

app = FastAPI()

@app.get("/sync-process")
def sync_process():
    time.sleep(10)
    
    return {"message": "Running sync process"}