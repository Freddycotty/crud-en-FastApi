from typing import List
from fastapi import APIRouter, Depends, status

from blog import oauth2
from .. import schemas, database
from sqlalchemy.orm import Session
from ..repository import BlogRepository

router = APIRouter(
    tags=['Blogs'],
    prefix='/blogs'
)


<<<<<<< HEAD
@router.get('/', status_code=200, response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(database.get_db)):
=======
@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
>>>>>>> parent of 9814f13 (Revert "[ADD] Autenticacion de rutas")
    return BlogRepository.get_all(db)


@router.post('/', status_code=201)
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
    return BlogRepository.create(request, db)


@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def show(id, db: Session = Depends(database.get_db)):
    return BlogRepository.show(id, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(database.get_db)):
    return BlogRepository.destroy(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(database.get_db)):
    return BlogRepository.update(id, request, db)
