"""
Database access layer (CRUD operations).

Keeping these separate from the route handlers keeps main.py / routers
thin and makes the query logic easy to unit test in isolation.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app import models, schemas


# ---------- Department CRUD ----------

def get_department(db: Session, department_id: int) -> Optional[models.Department]:
    return db.query(models.Department).filter(models.Department.id == department_id).first()


def get_departments(db: Session, skip: int = 0, limit: int = 100) -> List[models.Department]:
    return db.query(models.Department).offset(skip).limit(limit).all()


def create_department(db: Session, department: schemas.DepartmentCreate) -> models.Department:
    db_department = models.Department(**department.model_dump())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


def update_department(
    db: Session, department_id: int, updates: schemas.DepartmentUpdate
) -> Optional[models.Department]:
    db_department = get_department(db, department_id)
    if not db_department:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_department, field, value)
    db.commit()
    db.refresh(db_department)
    return db_department


def delete_department(db: Session, department_id: int) -> bool:
    db_department = get_department(db, department_id)
    if not db_department:
        return False
    db.delete(db_department)
    db.commit()
    return True


# ---------- Employee CRUD ----------

def get_employee(db: Session, employee_id: int) -> Optional[models.Employee]:
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()


def get_employee_by_email(db: Session, email: str) -> Optional[models.Employee]:
    return db.query(models.Employee).filter(models.Employee.email == email).first()


def get_employees(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    department_id: Optional[int] = None,
    status: Optional[models.EmployeeStatus] = None,
    search: Optional[str] = None,
) -> List[models.Employee]:
    query = db.query(models.Employee)

    if department_id is not None:
        query = query.filter(models.Employee.department_id == department_id)
    if status is not None:
        query = query.filter(models.Employee.status == status)
    if search:
        like = f"%{search}%"
        query = query.filter(
            or_(
                models.Employee.first_name.ilike(like),
                models.Employee.last_name.ilike(like),
                models.Employee.email.ilike(like),
                models.Employee.job_title.ilike(like),
            )
        )

    return query.offset(skip).limit(limit).all()


def create_employee(db: Session, employee: schemas.EmployeeCreate) -> models.Employee:
    db_employee = models.Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def update_employee(
    db: Session, employee_id: int, updates: schemas.EmployeeUpdate
) -> Optional[models.Employee]:
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_employee, field, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def delete_employee(db: Session, employee_id: int) -> bool:
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        return False
    db.delete(db_employee)
    db.commit()
    return True
