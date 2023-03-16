from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# ! Setup (Need if dont have Alembic setup)
# ! Auto creates tables if not created on save
# ! models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# Cors Middleware
# Everyone But Not Secure
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Default Route
@app.get("/")
def root():
    return {"message": "API up and running..."}
