from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db

# Router
router = APIRouter(prefix="/users", tags=["Users"])

# Routes
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash Password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    # New User (destructure)
    new_user = models.User(**user.dict())
    #! Validation
    # Add & Commit Post
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    # Find User
    user = db.query(models.User).filter(models.User.id == id).first()
    # Validation
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with ID: {id} does not exist"
        )
    return user
