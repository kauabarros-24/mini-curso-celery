from pydantic import BaseModel

class Email(BaseModel):
    to_email: str
    body: str
    subject: str