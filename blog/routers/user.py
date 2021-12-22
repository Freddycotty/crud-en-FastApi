from fastapi import APIRouter, Depends, status
from .. import schemas, database
from sqlalchemy.orm import Session
from ..repository import UserRepository


router = APIRouter(
    tags=['Users'],
    prefix='/user'
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    UserRepository.create(db, request)


@router.get('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ShowUser)
def show(id, db: Session = Depends(database.get_db)):
    return UserRepository.show(id, db)
