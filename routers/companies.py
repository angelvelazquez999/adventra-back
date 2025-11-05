from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db import get_db
from services.companies import CompaniesService
from schemas.companies import CompanyCreate, CompanyDB, CompanyList, CompanyUpdate

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post("/", response_model=CompanyDB, status_code=status.HTTP_201_CREATED)
def create_company(payload: CompanyCreate, db: Session = Depends(get_db)):
    svc = CompaniesService(db)
    return svc.create(payload)


@router.get("/", response_model=CompanyList)
def list_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    svc = CompaniesService(db)
    return svc.list(skip=skip, limit=limit)


@router.get("/{company_id}", response_model=CompanyDB)
def get_company(company_id: str, db: Session = Depends(get_db)):
    svc = CompaniesService(db)
    return svc.get(company_id)


@router.put("/{company_id}", response_model=CompanyDB)
def update_company(company_id: str, payload: CompanyUpdate, db: Session = Depends(get_db)):
    svc = CompaniesService(db)
    return svc.update(company_id, payload)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: str, db: Session = Depends(get_db)):
    svc = CompaniesService(db)
    svc.delete(company_id)
    return None
