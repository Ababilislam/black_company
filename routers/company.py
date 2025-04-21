from fastapi import APIRouter, Request, status, HTTPException,Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import psycopg

from model import models
from schema.schemas import User_out, User_in
from db.database import get_db
from sqlalchemy import func, text,desc
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles


router = APIRouter(
    prefix="/company",
    tags=["company"]
)
templates = Jinja2Templates(directory="templates")
# static file location
router.mount("/static", StaticFiles(directory="static"), name="static")

@router.get("/", response_model=list[User_out])
async def get_company(skip:int=0 , limit:int = 10, db:Session =Depends(get_db)):
    companies = db.query(models.Companies).order_by(desc(models.Companies.company_id)).offset(skip).limit(limit).all()
    if not companies:
        raise HTTPException(status_code=404, detail="companies not found")
    return companies


@router.get("/id/{company_id}", response_model=User_out)
def get_company_by_id(company_id: int, db =Depends(get_db)):
    company_query = db.query(models.Companies).filter(models.Companies.company_id == company_id)
    company = company_query.first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="company not found")
    return company

# search filter
@router.get("/filter/{company_name}", response_model=list[User_out])
def get_company_by_name(company_name: str, db =Depends(get_db)):
    # orm can't make use of group by with single column. need to use raw sql.
    company_query = db.execute(text("""SELECT DISTINCT ON (company_name) *FROM c_companies WHERE company_name ILIKE :name """), {"name": f"%{company_name}%"})
    # company_query = db.query(models.Companies.__table__.columns, func.count(models.Companies.company_name).label("num_of_company_group_together")).filter(models.Companies.company_name.ilike(f"%{company_name}%")).group_by(models.Companies.company_name)
    company = company_query.all()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"company not found with this '{company_name}' company name")
    return company 


@router.get("/{company_name}", response_model=list[User_out])
def get_company_by_name(company_name: str, db =Depends(get_db)):
    company_query = db.query(models.Companies).filter(models.Companies.company_name.ilike(f"%{company_name}%"))
    company = company_query.all()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"company not found with this '{company_name}' company name")
    return company


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_company(company: User_in, db=Depends(get_db)):
    # Check if the company already exists
    check_company_exists = db.query(models.Companies).filter(models.Companies.name == company.name, models.Companies.company_name == company.company_name).first()
    print(check_company_exists)
    if check_company_exists:    
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"'{company.company_name}' this Company already exists by this user:'{company.name}'s name")

    # Insert new company
    company_data = company.model_dump()
    new_company = models.Companies(**company_data)
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company


@router.get("/view/{company_name}")
async def get_company_view(request: Request,company_name:str):
    return templates.TemplateResponse(
        "details_view.html",
        {
            "request": request,
            "company_name": company_name,
        }
    )


import smtplib
from email.message import EmailMessage

@router.post("/send-message")
def message_send(title:str, message:str):
    sender_email = 'home.ayubul@gmail.com'
    sender_password = 'vyvd hgjp kdlq bcbf' #my g***l app pass

    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = 'ababilislamudoy@gmail.com'

    # msg data
    msg['Subject'] = title
    msg.set_content(message)
    # Send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)
    return msg