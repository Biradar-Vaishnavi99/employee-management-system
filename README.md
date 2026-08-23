# Employee Management System

A REST API for managing employees and departments, built with **FastAPI**, **SQLAlchemy**, and **SQLite**. Includes full CRUD operations, department–employee relationships, manager hierarchy, filtering, and search — with interactive API docs out of the box.

## Features

- **Departments**: create, list, retrieve (with nested employees), update, delete
- **Employees**: create, list, retrieve, update, delete
- Filter employees by department or status (`active`, `on_leave`, `resigned`, `terminated`)
- Search employees by name, email, or job title
- Manager → direct-report hierarchy (self-referential relationship)
- Input validation via Pydantic (e.g. valid email, positive salary)
- Auto-generated interactive docs (Swagger UI + ReDoc)
- CORS enabled for easy frontend integration

## Tech Stack

- **FastAPI** – web framework
- **SQLAlchemy** – ORM
- **SQLite** – database (file-based, zero setup; swappable for PostgreSQL/MySQL)
- **Pydantic** – request/response validation
- **Uvicorn** – ASGI server

## Project Structure

```
employee-management-system/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app, startup, router registration
│   ├── database.py        # DB engine/session setup
│   ├── models.py           # SQLAlchemy ORM models
│   ├── schemas.py          # Pydantic request/response schemas
│   ├── crud.py              # Database query logic
│   └── routers/
│       ├── __init__.py
│       ├── departments.py
│       └── employees.py
├── seed.py                # Optional script to populate sample data
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup & Run

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/employee-management-system.git
cd employee-management-system

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Seed the database with sample data
python seed.py

# 5. Run the server
uvicorn app.main:app --reload
```

The API will be running at `http://127.0.0.1:8000`.

- Interactive docs (Swagger UI): `http://127.0.0.1:8000/docs`
- Alternative docs (ReDoc): `http://127.0.0.1:8000/redoc`

## API Endpoints

### Departments
| Method | Endpoint | Description |
|---|---|---|
| POST | `/departments/` | Create a department |
| GET | `/departments/` | List all departments |
| GET | `/departments/{id}` | Get a department + its employees |
| PUT | `/departments/{id}` | Update a department |
| DELETE | `/departments/{id}` | Delete a department |

### Employees
| Method | Endpoint | Description |
|---|---|---|
| POST | `/employees/` | Create an employee |
| GET | `/employees/` | List employees (supports `department_id`, `status`, `search`, `skip`, `limit`) |
| GET | `/employees/{id}` | Get a single employee |
| PUT | `/employees/{id}` | Update an employee |
| DELETE | `/employees/{id}` | Delete an employee |

### Example: create a department and an employee

```bash
curl -X POST http://127.0.0.1:8000/departments/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Engineering", "description": "Builds the product"}'

curl -X POST http://127.0.0.1:8000/employees/ \
  -H "Content-Type: application/json" \
  -d '{
        "first_name": "Vaishnavi",
        "last_name": "Rao",
        "email": "vaishnavi@example.com",
        "phone": "9999999999",
        "job_title": "AI Engineer",
        "salary": 800000,
        "date_of_joining": "2025-01-15",
        "department_id": 1
      }'
```

## Switching to PostgreSQL/MySQL

By default the app uses SQLite (`employees.db`, created automatically). To use another database, set the `DATABASE_URL` environment variable before running, e.g.:

```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/employee_db"
uvicorn app.main:app --reload
```

## Possible Extensions

- JWT-based authentication and role-based access (admin/HR/employee)
- Pagination metadata (total count, next/prev links)
- Payroll and attendance tracking
- Alembic migrations for schema versioning
- Dockerfile for containerized deployment

## License

MIT — free to use for learning or as a portfolio project.
