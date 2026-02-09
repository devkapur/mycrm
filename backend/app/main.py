from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core import database

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True, 
)

@app.get("/")
def crm_root():
 
    return {"backend is working"}