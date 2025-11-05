from sqlalchemy import Column, String, Text, DateTime, ForeignKey, func
from db import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    legal_name = Column(String(255), nullable=False)
    rfc = Column(String(20), nullable=False)
    address = Column(Text)
    created_at = Column(DateTime, server_default=func.current_timestamp())
