from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, func
from typing import Optional
import uuid
from enum import Enum
from datetime import datetime

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(index=True, nullable=False, unique=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    email: str = Field(index=True, nullable=False)
    password: str = Field(nullable=False)
    photo_url: Optional[str] = None
    isverified: bool = Field(default=False)
    role : UserRole = Field(default=UserRole.USER, nullable=False)  
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: datetime = Field( sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()))
    
    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', email='{self.email}')"
    
 