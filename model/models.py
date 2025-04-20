from typing import Optional
from db.database import Base
from sqlalchemy import DateTime, Index, Integer, PrimaryKeyConstraint, String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime

class Base(DeclarativeBase):
    pass


class Companies(Base):
    __tablename__ = 'c_companies'
    __table_args__ = (
        PrimaryKeyConstraint('company_id', name='c_companies_pkey'),
        Index('c_name', 'employer_name')
    )

    company_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_name: Mapped[str] = mapped_column(String(255))
    rating: Mapped[int] = mapped_column(Integer, server_default=text('0'))
    post_status: Mapped[str] = mapped_column(String(10), server_default=text("'Active'::character varying"))
    name: Mapped[Optional[str]] = mapped_column(String(100))
    company_type: Mapped[Optional[str]] = mapped_column(String(100))
    details: Mapped[Optional[str]] = mapped_column(String(2500))
    office_location: Mapped[Optional[str]] = mapped_column(String(255))
    website_url: Mapped[Optional[str]] = mapped_column(String(255))
    phone_number: Mapped[Optional[str]] = mapped_column(String(20))
    email_address: Mapped[Optional[str]] = mapped_column(String(255))
    employer_name: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

