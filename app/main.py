from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import  engine
from .routers import event, user, auth, customer, instance, integration, platform, queue, responsecode, script, severity, modality

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["https://www.google.com","*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router)
app.include_router(event.router)
app.include_router(user.router)
app.include_router(customer.router)
app.include_router(instance.router)
app.include_router(integration.router)
app.include_router(platform.router)
app.include_router(queue.router)
app.include_router(responsecode.router)
app.include_router(script.router)
app.include_router(severity.router)
app.include_router(modality.router)

@app.get("/")
def root():
    return {"message": "Proactive Monitoring Fast API"}






