from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class ClientBase(BaseModel):
    names: str
    lastname: str
    document_type: str
    document_number: str
    email: Optional[str] = None
    phone: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: UUID
    class Config:
        orm_mode = True

class LawyerBase(BaseModel):
    names: str
    lastnames: str
    field: Optional[str] = None
    email: str

class LawyerCreate(LawyerBase):
    pass

class Lawyer(LawyerBase):
    id: UUID
    num_cases: int = 0
    available: bool = True
    class Config:
        orm_mode = True

class CaseBase(BaseModel):
    title: str
    description: Optional[str] = None
    state: str = "open"
    priority: int = 3

class CaseCreate(CaseBase):
    lawyer_id: UUID
    client_id: UUID

class Case(CaseBase):
    id: UUID
    lawyer_id: UUID
    client_id: UUID
    date_created: datetime
    date_updated: Optional[datetime] = None
    class Config:
        orm_mode = True

class ReceiptBase(BaseModel):
    amount: float
    ruc_enterprise: Optional[str] = None
    ruc_client: Optional[str] = None

class ReceiptCreate(ReceiptBase):
    case_id: UUID

class Receipt(ReceiptBase):
    id: UUID
    case_id: UUID
    date: datetime
    file_path: Optional[str] = None
    class Config:
        orm_mode = True