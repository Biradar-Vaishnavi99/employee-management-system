from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.post("/", response_model=schemas.Department, status_code=201)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    existing = db.query(crud.models.Department).filter(
        crud.models.Department.name == department.name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Department name already exists")
    return crud.create_department(db, department)


@router.get("/", response_model=List[schemas.Department])
def list_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_departments(db, skip=skip, limit=limit)


@router.get("/{department_id}", response_model=schemas.DepartmentWithEmployees)
def get_department(department_id: int, db: Session = Depends(get_db)):
    department = crud.get_department(db, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@router.put("/{department_id}", response_model=schemas.Department)
def update_department(
    department_id: int, updates: schemas.DepartmentUpdate, db: Session = Depends(get_db)
):
    department = crud.update_department(db, department_id, updates)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@router.delete("/{department_id}", status_code=204)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_department(db, department_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Department not found")
    return None
