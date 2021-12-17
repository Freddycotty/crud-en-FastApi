from fastapi import FastAPI
from pydantic import BaseModel
from typing import Text, Optional
from datetime import date, datetime
import uvicorn
app = FastAPI()
posts = []


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


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


@app.post('/blog')
def index(blog: Blog):
    return {'data': f'Blog is created with the title as {blog.title}'}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
