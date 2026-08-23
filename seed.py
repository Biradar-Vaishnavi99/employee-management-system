"""
Optional helper script to populate the database with sample data,
so the API isn't empty when you first explore it or record a demo.

Run with:
    python seed.py
"""

from datetime import date

from app.database import SessionLocal, engine, Base
from app import models

Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    if db.query(models.Department).count() > 0:
        print("Database already has data. Skipping seed.")
    else:
        engineering = models.Department(name="Engineering", description="Builds and maintains products")
        hr = models.Department(name="Human Resources", description="Hiring and employee relations")
        sales = models.Department(name="Sales", description="Revenue and client relationships")
        db.add_all([engineering, hr, sales])
        db.commit()
        db.refresh(engineering)
        db.refresh(hr)
        db.refresh(sales)

        manager = models.Employee(
            first_name="Ananya", last_name="Sharma", email="ananya.sharma@example.com",
            phone="9876543210", job_title="Engineering Manager", salary=1800000,
            date_of_joining=date(2021, 6, 1), department_id=engineering.id,
        )
        db.add(manager)
        db.commit()
        db.refresh(manager)

        employees = [
            models.Employee(
                first_name="Rohan", last_name="Verma", email="rohan.verma@example.com",
                phone="9876500001", job_title="Backend Developer", salary=1100000,
                date_of_joining=date(2022, 3, 15), department_id=engineering.id,
                manager_id=manager.id,
            ),
            models.Employee(
                first_name="Priya", last_name="Nair", email="priya.nair@example.com",
                phone="9876500002", job_title="Frontend Developer", salary=1050000,
                date_of_joining=date(2023, 1, 10), department_id=engineering.id,
                manager_id=manager.id,
            ),
            models.Employee(
                first_name="Kabir", last_name="Singh", email="kabir.singh@example.com",
                phone="9876500003", job_title="HR Executive", salary=700000,
                date_of_joining=date(2022, 8, 20), department_id=hr.id,
            ),
            models.Employee(
                first_name="Meera", last_name="Iyer", email="meera.iyer@example.com",
                phone="9876500004", job_title="Sales Executive", salary=650000,
                date_of_joining=date(2023, 5, 5), department_id=sales.id,
            ),
        ]
        db.add_all(employees)
        db.commit()

        print("Seeded 3 departments and 5 employees.")
finally:
    db.close()
