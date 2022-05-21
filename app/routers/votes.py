from http.client import HTTPConnection
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import schemas, database, models, oauth2
from .. import models, schemas, utils
from .. database import get_db

router = APIRouter(
    prefix='/vote',  # -replace specifying the url dir in each request
    tags=['vote']  # -grouping votes.py routes in the /docs url
)

@router.post("/", status_code = status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  
  post_exists = db.query(models.Post).filter(vote.post_id == models.Post.id).first()
  if post_exists is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Post does not exist')

  #select * from votes where user_id = ? and post_id = ?
  vote_query = db.query(models.Vote).filter(
      models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

  found_vote = vote_query.first()

  #if the action was to vote
  if (vote.dir == 1):
    if found_vote:
      raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f'user {current_user.id} has already voted on post {vote.post_id}')
    
    new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
    db.add(new_vote)
    db.commit()
    return {"message": "successfully added vote"}

  #if the action was to delete vote
  else:
    if not found_vote:
      raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'vote does not exist')
    vote_query.delete(synchronize_session=False)
    db.commit()
    return {"message" "successfully deleted vote"}
      
