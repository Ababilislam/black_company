from fastapi import Depends, FastAPI, requests
from model import models
from db.database import get_db
from db.database import engine
from routers import company
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)   #hides the docs,redoc and openapi.json
# app = FastAPI()

# add fontend templates
templates = Jinja2Templates(directory="templates")
# static file location
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(company.router)


@app.get("/")
async def root(db:Session=Depends(get_db)):
    
    # return {"message": "Welcome to Black company API"}
    return templates.TemplateResponse("home.html", {"request": {"title":"Home page"}})




