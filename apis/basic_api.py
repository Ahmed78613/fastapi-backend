# Basic Type Of API (NOT RUNNING)
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from uuid import uuid4

app = FastAPI()

# Model
class Post(BaseModel):
    title: str
    content: str
    published: bool = True # Default

# Database
my_posts = [
    {
     "id": "a31ab0b8-1bc1-4599-85c2-6e4dcd27f14a", 
     "title": "First Post", 
     "content": "Description goes in here...",
     }, 
    {
     "id": "426bd0d3-4ed1-4ce1-8c81-013c33a2aba7", 
     "title": "Favorite Food", 
     "content": "Pizza",
     }, 
]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
        
def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index

# Routes
@app.get("/")
def root():
    return {"message": "API up and running..."}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # Create ID
    post_dict = post.dict()
    post_dict["id"] = uuid4()
    # Store Post
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: str):
    # Find post
    post = find_post(id)
    # Validation
    if not post:
        raise HTTPException(status_code=404,detail=f"Sorry, ID: {id} was not found")
    else:
        return {"post_detail": post}
    
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: str):
    # Delete post
    index = find_index_post(id)
    # Validation
    if index == None:
        raise HTTPException(status_code=404,detail=f"Sorry, Post with ID: {id} does not exist")
    else:
        my_posts.pop(index)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: str, post: Post):
    # Find Post
    index = find_index_post(id)
    # Validation
    if index == None:
        raise HTTPException(status_code=404,detail=f"Sorry, Post with ID: {id} does not exist")
    else:
    # Update Post
        post_dict = post.dict()
        my_posts[index] = post_dict
        post_dict["id"] = id
        return {"data": post_dict}