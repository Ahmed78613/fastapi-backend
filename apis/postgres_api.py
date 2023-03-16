# PostgreSQL API (NOT RUNNING)
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# Model
class Post(BaseModel):
    title: str
    content: str
    published: bool = True # Default

 # Connect to an existing database
while True: 
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="password123", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)

# Routes
@app.get("/")
def root():
    return {"message": "API up and running..."}

@app.get("/posts")
def get_posts():
    # SQL Query
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # SQL Query
    cursor.execute(
    """ 
    INSERT INTO posts (title, content, published) 
    VALUES (%s, %s, %s) 
    RETURNING *
    """, (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    print(new_post)
    # Save Data
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int):
    # SQL Query ("," fixes some issues)
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    # Validation
    if not post:
        raise HTTPException(status_code=404,detail=f"Post with ID: {id} was not found")
    return {"post_detail": post}
    
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # SQL Query ("," fixes some issues)
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    # Validation
    if deleted_post == None:
        raise HTTPException(status_code=404,detail=f"Sorry, Post with ID: {id} does not exist")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # SQL Query
    cursor.execute(
        """
        UPDATE posts 
        SET title = %s, content = %s, published = %s
        WHERE id = %s
        RETURNING *
        """, 
    (post.title, post.content, post.published, str(id)))
    
    updated_post = cursor.fetchone()
    conn.commit()
    
    # Validation
    if updated_post == None:
        raise HTTPException(status_code=404,detail=f"Post with ID: {id} does not exist")
    else:
        return {"data": updated_post}