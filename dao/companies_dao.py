from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from models.companies import Company


class CompaniesDAO:
	"""DAO simple para operaciones CRUD de companies.

	Esta clase no crea su propia sesión: se le debe pasar una Session en el constructor
	o se debe construir la instancia desde el service pasándole `db`.
	"""

	def __init__(self, db: Session):
		self.db = db

	def get(self, company_id: str) -> Optional[Company]:
		return self.db.query(Company).filter(Company.id == company_id).first()

	def list(self, skip: int = 0, limit: int = 100) -> List[Company]:
		return self.db.query(Company).offset(skip).limit(limit).all()

	def create_from_dict(self, data: Dict[str, Any]) -> Company:
		obj = Company(**data)
		self.db.add(obj)
		self.db.commit()
		self.db.refresh(obj)
		return obj

	def update(self, obj: Company) -> Company:
		# obj is assumed to be attached to the session
		self.db.add(obj)
		self.db.commit()
		self.db.refresh(obj)
		return obj

	def delete(self, obj: Company) -> None:
		self.db.delete(obj)
		self.db.commit()

