from fastapi import FastAPI
from .database import engine, Base
from . import models
from .routers import users, auth ,vaccine, appointment, vaccination, awareness_article


app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vaccine.router)
app.include_router(appointment.router)
app.include_router(vaccination.router)
app.include_router(awareness_article.router)

@app.get("/")
def root():
    return {"message": "Vaccination API is running"}
