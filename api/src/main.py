from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel, validator
import openai
import os
from sqlalchemy.orm import Session
from .database import engine, SessionLocal, get_db
from .schemas import QueryRequest, QueryResponse, User
from .auth import authenticate_user, create_access_token
from .core.query.services.query_service import process_query as query_service

app = FastAPI()

# Authentication Route
@app.post("/login")
async def login(user: User, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()
    if not user_db or not user_db.check_password(user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user_db.email})
    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"})

# Query Processing Route
@app.post("/query", dependencies=[Depends(authenticate_user)])
async def process_query(query_request: QueryRequest, db: Session = Depends(get_db)):
    response = await query_service(query_request, db)
    return JSONResponse(content={"query_id": response.id, "response": response.response})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)