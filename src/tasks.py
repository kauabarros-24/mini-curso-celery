import time
from celery import Celery
from src.config import REDIS_URL, MAILTRAP
import mailtrap as mt
import asyncio

celery_app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)

client_mt = mt.MailtrapClient(token=MAILTRAP["token"])

@celery_app.task
def long_task():
    time.sleep(10)
    
    return {"message": "Finished tasks with celery"}

@celery_app.task
def process_data_and_sending_email(subject, body, to_email):
    asyncio.run(send_email(to_email, subject, body))
    return {"Task do celery finalizada": "message"}

async def send_email(to_email, subject, body):
    mail = mt.Mail(
        sender=mt.Address(email="mailtrap@demomailtrap.co", name="Mailtrap Test"),
        to=[mt.Address(email=to_email, name="User")],
        subject=subject,
        text=body,
    )
    try:
        client_mt.send(mail)
        print("Envio de email feito")
    except Exception as error:
        print(f"Não deu certo: {error}")
        
@celery_app.task(bind=True)
def long_task_with_progress(self, total: int = 100):
    import time
    for i in range(total):
        time.sleep(1)
        self.update_state(state="PROGRESS", meta={"current": i, "total": total})
    return {"status": "completed"}
        

    