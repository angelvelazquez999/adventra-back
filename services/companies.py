from typing import Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import uuid

from dao.companies_dao import CompaniesDAO
from schemas.companies import CompanyCreate, CompanyUpdate


class CompaniesService:
    def __init__(self, db: Session):
        self.db = db
        self.dao = CompaniesDAO(db)

    def create(self, payload: CompanyCreate) -> Any:
        # Generar id si no viene
        new_id = payload.id or str(uuid.uuid4())
        data = payload.dict()
        data["id"] = new_id
        company = self.dao.create_from_dict(data)
        return company

    def get(self, company_id: str) -> Any:
        company = self.dao.get(company_id)
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        return company

    def list(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        items = self.dao.list(skip=skip, limit=limit)
        total = len(items)
        return {"items": items, "total": total}

    def update(self, company_id: str, payload: CompanyUpdate) -> Any:
        company = self.dao.get(company_id)
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        update_data = payload.dict(exclude_unset=True)
        for k, v in update_data.items():
            setattr(company, k, v)
        return self.dao.update(company)

    def delete(self, company_id: str) -> None:
        company = self.dao.get(company_id)
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        self.dao.delete(company)
