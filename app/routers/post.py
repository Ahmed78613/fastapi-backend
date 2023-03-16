from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from .. import models, schemas, oauth2
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db


# Router
router = APIRouter(prefix="/posts", tags=["Posts"])

# Routes
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # *Find & Apply Parameters (Without count & Join)
    # *posts = (
    # *    db.query(models.Post)
    # *    .filter(models.Post.owner_id == current_user.id)
    # *    .filter(models.Post.title.contains(search))
    # *    .limit(limit)
    # *    .offset(skip)
    # *    .all()
    # *)

    # Left Outer Join With Count & Params
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # New Post (destructure)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    # Add & Commit Post
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # Find Post By ID
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )
    # Validation
    if not post:
        raise HTTPException(
            status_code=404, detail=f"Post with ID: {id} does not exist"
        )
    # * Check User is Post Owner (Validation)
    # * if post[0].owner_id != current_user.id:
    # *     raise HTTPException(
    # *         status_code=status.HTTP_403_FORBIDDEN,
    # *         detail="Not authorized to perform requested action",
    # *     )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # Find Post By ID
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    # Check Post Exists (Validation)
    if post == None:
        raise HTTPException(
            status_code=404, detail=f"Post with ID: {id} does not exist"
        )
    # Check User is Post Owner (Validation)
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    # Delete Post & Commit
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # Find Post By ID
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    # Check Post Exists (Validation)
    if post == None:
        raise HTTPException(
            status_code=404, detail=f"Post with ID: {id} does not exist"
        )
    # Check User is Post Owner (Validation)
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    # Update & Commit Post
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
