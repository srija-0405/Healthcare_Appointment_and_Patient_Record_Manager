import re
from datetime import datetime
from random import randint

PHONE_REGEX = re.compile(r'^[6-9]\d{9}$')

def format_date(d: datetime):
    if not d:
        return ""
    return d.strftime("%Y-%m-%d")

def validate_phone(phone: str) -> bool:
    if not phone:
        return False
    return bool(PHONE_REGEX.match(phone.strip()))

def generate_patient_id(prefix="P"):
    return f"{prefix}{randint(1000,9999)}"
