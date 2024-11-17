from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from user_services import schemas, user_service, database,model
from user_services.database import get_db

app = FastAPI()

# Create the tables in the database
model.Base.metadata.create_all(bind=database.engine)

# Register User Endpoint
@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_service.register_user(db=db, user=user)

# Login Endpoint
@app.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    return user_service.login_user(db=db, email=email, password=password)

# Profile Update Endpoint
@app.put("/profile")
def update_profile(user_update: schemas.UserUpdate, db: Session = Depends(get_db), user_id: int = Depends(user_service.get_user_from_token)):
    return user_service.update_user_profile(db=db, user_id=user_id, user_update=user_update)
