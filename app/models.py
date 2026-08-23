"""
SQLAlchemy ORM models: Department and Employee.

An Employee belongs to a Department (many-to-one), and can optionally
report to another Employee (self-referential manager relationship).
"""

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class EmployeeStatus(str, enum.Enum):
    ACTIVE = "active"
    ON_LEAVE = "on_leave"
    RESIGNED = "resigned"
    TERMINATED = "terminated"


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)

    employees = relationship(
        "Employee", back_populates="department", cascade="all, delete-orphan"
    )


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    job_title = Column(String(100), nullable=False)
    salary = Column(Float, nullable=False)
    date_of_joining = Column(Date, nullable=False)
    status = Column(Enum(EmployeeStatus), default=EmployeeStatus.ACTIVE, nullable=False)

    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    department = relationship("Department", back_populates="employees")

    manager_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    manager = relationship("Employee", remote_side=[id], backref="direct_reports")
