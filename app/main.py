from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


my_posts = [{"title": "first", "content": "first_data", "published": True, "rating": 4, "id":1}, 
            {"title": "second", "content": "second_data", "published": True, "rating": 4, "id":2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_post_index(id):
    for i, p, in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"The post id {id} was not found")
    return {"post_details": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # find the index in the array that has required id
    # my_posts.pop(index)
    index = find_post_index(id)
    if not index:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post id {id} not found in database")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    index = find_post_index(id)
    if not index:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post id {id} not found in database")
    post_dict = post.model_dump()
    print(f"post_dict : {post_dict}")
    post_dict["id"] = id
    print(f"post_dict : {post_dict}")
    print(f"my_posts[index] : {my_posts[index]}")
    my_posts[index] = post_dict
    print(f"my_posts[index] : {my_posts[index]}")
    return {"data": post_dict}