from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from blog import models, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash
app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=201, tags=['Blog'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', status_code=200, response_model=List[schemas.ShowBlog], tags=['Blog'])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=['Blog'])
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'blog whit the id {id} is not available')
    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blog'])
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog whit id {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return {'message': 'Delete successfully!'}


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Blog'])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog whit id {id} not found')
    blog.update(request.dict())
    db.commit()
    return 'updated'


@app.post('/user', status_code=status.HTTP_201_CREATED, tags=['User'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ShowUser, tags=['User'])
def show(id, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User whit the id {id} is not available')
    return user
