from pydantic import BaseModel, EmailStr
from datetime import date


class Recipient(BaseModel):
    name: str
    email: EmailStr


class GenerationRequest(BaseModel):
    event_name: str
    date: date
    recipients: list[Recipient]