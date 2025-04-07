from fastapi import FastAPI,requests, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from pydantic import BaseModel
import random
from fastapi import FastAPI
from quiz_routes import router 
from sudoku_routes import sudoku_router  # ✅ import your new router
from addition_routes import router as addition_router
from subtraction_routes import router as subtraction_router
from multiplication_routes import router as multiplication_router
from division_routes import router as division_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from autodidact!"}

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend origin in prod

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all quiz-related routes
app.include_router(router)

app.include_router(addition_router)  
app.include_router(subtraction_router)
app.include_router(division_router)
app.include_router(multiplication_router)
app.include_router(sudoku_router)  
