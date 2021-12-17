from fastapi import FastAPI
from pydantic import BaseModel
from typing import Text, Optional
from datetime import date, datetime

app = FastAPI()
posts = []


class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False


@app.get('/blog')
def index(limit=10, published: bool = True, sort: Optional[str] = None):
    if published:
        print(sort)
        return {'data': f'{limit} published blogs from the db'}
    return {'data': f'{limit} blogs from the db'}


@app.get('/blog/{id}')
def get_posts(id):
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id, limit=10):
    print(limit)
    return {'data': {'1', '2', }}
