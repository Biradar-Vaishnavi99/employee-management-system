"""
Pydantic schemas used for request validation and response serialization.
"""

from datetime import date
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

from app.models import EmployeeStatus


# ---------- Department ----------

class DepartmentBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=255)


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=255)


class Department(DepartmentBase):
    id: int

    class Config:
        from_attributes = True


class DepartmentWithEmployees(Department):
    employees: List["EmployeeBrief"] = []

    class Config:
        from_attributes = True


# ---------- Employee ----------

class EmployeeBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    job_title: str = Field(..., max_length=100)
    salary: float = Field(..., gt=0)
    date_of_joining: date
    status: EmployeeStatus = EmployeeStatus.ACTIVE
    department_id: int
    manager_id: Optional[int] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    job_title: Optional[str] = Field(None, max_length=100)
    salary: Optional[float] = Field(None, gt=0)
    date_of_joining: Optional[date] = None
    status: Optional[EmployeeStatus] = None
    department_id: Optional[int] = None
    manager_id: Optional[int] = None


class EmployeeBrief(BaseModel):
    """Lightweight representation, used to avoid deep nesting/recursion."""
    id: int
    first_name: str
    last_name: str
    job_title: str

    class Config:
        from_attributes = True


class Employee(EmployeeBase):
    id: int
    department: Department

    class Config:
        from_attributes = True


DepartmentWithEmployees.model_rebuild()
