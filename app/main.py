from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud, database

# Initialize the app and database
app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# @app.put("/users/{user_id}/email", response_model=schemas.User)
# def update_email(user_id: int, new_email: str, db: Session = Depends(get_db)):
#     # Cek apakah email baru sudah terdaftar
#     existing_user = crud.get_user_by_email(db, email=new_email)
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already in use")

#     # Update email
#     updated_user = crud.update_user_email(db, user_id=user_id, new_email=new_email)
#     if not updated_user:
#         raise HTTPException(status_code=404, detail="User not found")

#     return updated_user

