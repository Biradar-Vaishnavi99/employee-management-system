from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app import crud, schemas, models
from app.database import get_db

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("/", response_model=schemas.Employee, status_code=201)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    if crud.get_employee_by_email(db, employee.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if not crud.get_department(db, employee.department_id):
        raise HTTPException(status_code=404, detail="Department not found")
    if employee.manager_id and not crud.get_employee(db, employee.manager_id):
        raise HTTPException(status_code=404, detail="Manager (employee) not found")
    return crud.create_employee(db, employee)


@router.get("/", response_model=List[schemas.Employee])
def list_employees(
    skip: int = 0,
    limit: int = 100,
    department_id: Optional[int] = None,
    status: Optional[models.EmployeeStatus] = None,
    search: Optional[str] = Query(None, description="Search by name, email, or job title"),
    db: Session = Depends(get_db),
):
    return crud.get_employees(
        db, skip=skip, limit=limit, department_id=department_id, status=status, search=search
    )


@router.get("/{employee_id}", response_model=schemas.Employee)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = crud.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.put("/{employee_id}", response_model=schemas.Employee)
def update_employee(
    employee_id: int, updates: schemas.EmployeeUpdate, db: Session = Depends(get_db)
):
    if updates.department_id and not crud.get_department(db, updates.department_id):
        raise HTTPException(status_code=404, detail="Department not found")
    employee = crud.update_employee(db, employee_id, updates)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.delete("/{employee_id}", status_code=204)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_employee(db, employee_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Employee not found")
    return None
