from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/blog', status_code=200, response_model=List[schemas.ShowBlog], tags=['Blog'])
def all(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post('/blog', status_code=201, tags=['Blog'])
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=['Blog'])
def show(id, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'blog whit the id {id} is not available')
    return blog


@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blog'])
def destroy(id, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog whit id {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return {'message': 'Delete successfully!'}


@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Blog'])
def update(id, request: schemas.Blog, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog whit id {id} not found')
    blog.update(request.dict())
    db.commit()
    return 'updated'
