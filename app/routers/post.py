from tkinter import TRUE
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func 
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from .. database import get_db

#--used to reference the post.py path operations in main.py
#--@app decorator in main.py is replaced with @router decorator here
router = APIRouter(
  prefix = '/posts', #-replace specifying the posts dir in each request
  tags = ['Posts'] #-grouping post.py routes in the /docs url
)

##-GET ALL POSTS------------------------------------------------------
# http://127.0.0.1:8000/posts


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
  row_limit: int = 10, 
  skip:int = 0,
  search: Optional[str] = '',
  min_votes:int = 0):
  #posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
  # #select * from posts limit row_limit

  #select  from votes left join posts on votes.post_id = posts.id
  posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')) \
    .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
    .filter(models.Post.title.contains(search)) \
    .group_by(models.Post.id) \
    .having(func.count(models.Vote.post_id) >= min_votes) \
    .offset(skip) \
    .limit(row_limit) \
    .all()
    
  return posts  # returns json in browser


##-CREATE NEW POST----------------------------------------------------
  ##--users need to be logged in to create a post

  ##-- oauth2.get_current_user dependency forces user to be logged in. returns nothing (no error) or credentials exception error (token not validated).
  ##-- get_current_user() executes the verify_access_token() function to verify user's token

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, 
  db: Session = Depends(get_db), 
  current_user: int = Depends(oauth2.get_current_user) ):

  #--accept 2 parameters, post object (post) and a persistent session (db)
  #--create new post, add it to the database, commit the change,
  # unpacks to  title = post.title, content = post.content, published = post.published
  new_post = models.Post(user_id = current_user.id, **post.dict())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post


##-GET POST BY ID--------------------------------------------------------
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

  #post = db.query(models.Post).filter(models.Post.id == id).first()
  post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')) \
      .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
      .group_by(models.Post.id) \
      .filter(models.Post.id == id).first()
        
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="post with id {} was not found".format(id))
  return post


##-DELETE POST---------------------------------------------------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()

  if post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="post with id {} was not found".format(id))

  if post.user_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail='Not authorized to perform requested action.')

  post_query.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)


##-PUT UPDATE TO POST---------------------------------------------------
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()

  if post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="post with id {} was not found".format(id))

  if post.user_id != current_user.id:  # oauth2.get_current_user.id
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail='Not authorized to perform requested action.')

  post_query.update(updated_post.dict(), synchronize_session=False)
  db.commit()
  return post_query.first()
