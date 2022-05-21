###--ORIGINAL IMPLEMENTATION USING STRAIGHT SQL WITHOUT ORM--#

import http
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from time import sleep
##--POSTGRES CONNECTION MODULES
import psycopg2
from psycopg2.extras import RealDictCursor ##--REQUIRED TO GET COLUMN NAMES--

#module on LOCALHOST---------------------
app = FastAPI()

#----CONNECTION TO POSTGRES-------------
while True:
  try:
    conn = psycopg2.connect(host='localhost',
                            database='fastapi',
                            user='postgres',
                            password='302kenyon',
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print('database conection was successful')
    break
  except Exception as error:
    print('connecting to database failed')
    print('Error: ', error)
    time.sleep(2)

##--extension of BaseModel to fit POST data---------------------------------------------------
class Post(BaseModel):
  title: str
  content: str
  published: bool = True 
  rating: Optional[int] = None 

#sample data -------
my_posts = [{"title":"title of post1", "content":"content of post 1", "id":1},
            {"title": "favorite foods", "content": "i like pizza", "id": 2},
]

############-------------------------------------------------------------------------------
##--API END POINTS-------------------------------------------------------------------------

##-ROOT DIRECTORY--------------------------------------------------------------------------------
@app.get("/") #http://127.0.0.1:8000/
def root():
  return {"message":"welcome to my api!!!"} #returns json in browner

##-GET ALL POSTS--------------------------------------------------------------------------------
@app.get("/posts") #http://127.0.0.1:8000/posts
def get_posts():
  cursor.execute(""" select * from posts """)
  posts = cursor.fetchall()

  return {"data": posts } #returns json in browser

##-CREATE NEW POST--------------------------------------------------------------------------------
@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
  cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    (post.title, post.content, post.published))
  new_post = cursor.fetchone()
  conn.commit() #commit to save change. otherwise the value will show in postman but nothing is saved

  return {"data": new_post}

##-GET POST BY ID--------------------------------------------------------------------------------
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
  cursor.execute(""" SELECT title, content, published FROM posts WHERE id = %s """, (str(id),))
  post = cursor.fetchone()

  if not post:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = "post with id {} was not found".format(id))

  return {"post_detail": post}

##-DELETE POST--------------------------------------------------------------------------------
@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

  cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *;""", (str(id), ))
  deleted_post = cursor.fetchone()
  conn.commit()

  if deleted_post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="post with id {} was not found".format(id))

  return Response(status_code = status.HTTP_204_NO_CONTENT)

##-PUT UPDATE TO POST--------------------------------------------------------------------------------
@app.put("/posts/{id}", status_code = status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):

  cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    (post.title, post.content, post.published, str(id)))
  updated_post = cursor.fetchone()
  conn.commit() #commit to save change. otherwise the value will show in postman but nothing is saved

  if updated_post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="post with id {} was not found".format(id))
  return {"data:": updated_post} 


