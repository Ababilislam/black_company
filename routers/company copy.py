from fastapi import APIRouter, status, HTTPException,Depends
import psycopg

from model import models
from schema.schemas import User_out, User_in
from db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/company",
    tags=["company"]
)

@router.get("/{company_id}", response_model=User_out)
def get_user(company_id: int, db =Depends(get_db)):
    company_query = db.query(models.Companies).filter(models.Companies.company_id == company_id)
    company = company_query.first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="company not found")
    return company

@router.get("/", response_model=list[User_out])
def get_user(db =Depends(get_db)):
    companies = db.query(models.Companies).all()
    if not companies:
        raise HTTPException(status_code=404, detail="companies not found")
    return companies

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_company(company: User_in, db=Depends(get_db)):
    cursor, conn = db

    # Check if the company already exists
    # cursor.execute("SELECT 1 FROM c_companies WHERE name = %s AND company_name = %s",
    # (company.name, company.company_name))
    # result = cursor.fetchall()
    check_company_exists = db.query(models.Companies).filter(models.Companies.name == company.name, models.Companies.company_name == company.company_name)
    print(check_company_exists)
    # if result:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company already exists by this user name")

    # Insert new company
    # cursor.execute(
    #     "INSERT INTO c_companies (name,company_name, company_type, details, rating, office_location, website_url, phone_number, email_address, employer_name) "
    #     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    #     (
    #         company.name, company.company_name, company.company_type, company.details, company.rating, company.office_location,
    #         company.website_url, company.phone_number, company.email_address,
    #         company.employer_name
    #     )
    # )
    # conn.commit()

    # Get the newly inserted record
    # company_id = cursor.lastrowid
    # cursor.execute("SELECT * FROM c_companies WHERE company_id = %s", (company_id,))
    # new_company = cursor.fetchone()
    # print(new_company)
    return "new_company"