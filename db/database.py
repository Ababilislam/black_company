from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# sql_alchemy_database_url = "postgresql+psycopg://ab:1212@localhost:5432/postgres"
# sql_alchemy_database_url = "postgresql+psycopg://postgres.mrqikljawdijdpsvhfpy:Absqldb@12@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
sql_alchemy_database_url = "postgresql+psycopg://postgres.mrqikljawdijdpsvhfpy:Absqldb%4012@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
engine = create_engine(sql_alchemy_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()