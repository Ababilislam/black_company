from datetime import datetime
from pydantic import BaseModel


class User_out(BaseModel):
    company_id: int
    name: str|None
    company_name: str
    company_type: str|None
    details: str|None
    rating: int
    office_location: str|None
    website_url: str|None
    phone_number: str|None
    email_address: str|None
    employer_name: str|None
    created_at: datetime|None
    updated_at: datetime|None

class User_in(BaseModel):
    name: str|None
    company_name: str
    company_type: str|None
    details: str|None
    rating: int|None
    office_location: str|None
    website_url: str|None
    phone_number: str|None
    email_address: str|None
    employer_name: str|None