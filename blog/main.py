from fastapi import FastAPI
from .schemas import Blog
from blog import models
from .database import engine
app = FastAPI()

models.Base.metadata.create_all(engine)


@app.post('/blog')
def create(request: Blog):

    return request
