"""
Employee Management System — FastAPI application entrypoint.

Run with:
    uvicorn app.main:app --reload

Then open http://127.0.0.1:8000/docs for interactive Swagger UI.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import employees, departments

# Create tables on startup (fine for SQLite/dev; use Alembic migrations in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management System",
    description="A simple REST API to manage employees and departments.",
    version="1.0.0",
)

# Allow all origins in dev; restrict this in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(departments.router)
app.include_router(employees.router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Employee Management System API is running", "docs": "/docs"}
