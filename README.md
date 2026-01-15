# Vaccination_Pasteur Platform

## 📌 Project Description
This project is a backend web application built with FastAPI to manage vaccination processes.
It allows citizens to book vaccination appointments and administrators to manage vaccines,
appointments, vaccinations, and awareness articles.

The system uses OAuth2 authentication, role-based access control, and PostgreSQL as the database.

## 🛠️ Technologies Used
- Python 3
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Alembic (Database Migrations)
- OAuth2 & JWT Authentication
- Pydantic
- Swagger UI (OpenAPI)

## Features
- User management (citizen / admin)
- Appointment scheduling
- Vaccination tracking
- Vaccine management
- Awareness articles


## 🔐 Authentication & Authorization

The application uses OAuth2 with JWT tokens for authentication.

### Roles:
- **Admin**: Can manage vaccines, approve appointments, register vaccinations,
  and create awareness articles.
- **Citizen**: Can register, book appointments, and view vaccination history.

Access to endpoints is controlled using FastAPI dependencies.



## 🗄️ Database & Migrations

The project uses PostgreSQL as the database and Alembic for schema migrations.

### Create migration:
```bash
alembic revision --autogenerate -m "initial tables"
