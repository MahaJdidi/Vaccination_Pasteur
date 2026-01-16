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
- Docker & Docker Compose

## Features
- User authentication (JWT)
- Role-based access (Admin / User)
- Vaccination appointment booking
- Vaccine and vaccination management
- Awareness articles
- PostgreSQL database
- Alembic migrations
- Dockerized deployment
- Interactive API documentation with Swagger


## 🔐 Authentication & Authorization

The application uses OAuth2 with JWT tokens for authentication.

### Roles:
- **Admin**: Can manage vaccines, approve appointments, register vaccinations,
  and create awareness articles.
- **Citizen**: Can register, book appointments, and view vaccination history.

Access to endpoints is controlled using FastAPI dependencies.


## Run Locally with Docker

docker compose up --build
API available at: http://localhost:8000
Swagger UI: http://localhost:8000/docs


## 🗄️ Database & Migrations

Migrations are handled automatically at container startup using Alembic.
