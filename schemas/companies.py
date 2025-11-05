from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CompanyBase(BaseModel):
    user_id: str
    legal_name: str
    rfc: str
    address: Optional[str] = None


class CompanyCreate(CompanyBase):
    # id puede ser generado por la app (UUID)
    id: Optional[str] = None


class CompanyUpdate(BaseModel):
    legal_name: Optional[str] = None
    rfc: Optional[str] = None
    address: Optional[str] = None


class CompanyDB(CompanyBase):
    id: str
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class CompanyList(BaseModel):
    items: List[CompanyDB]
    total: int
