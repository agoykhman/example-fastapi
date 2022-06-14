from app.main import app
import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.oauth2 import create_access_token
from app.database import Base, get_db
from app import models 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# get_db() ONLY for reference for the override
from app.database import get_db, Base

#--TEST CONNECTION STRING
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_user_name}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

#--TEST ENV connection engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


#!-SESSION fixture
# drop, re-create all tables & establish new session.
  #- default schope is "function" so tables are created and dropped with each test.
  #-- if you set scope to "session" or "module" the fixture will run only once
  #--- but then the tests are correlated. user_login_test is dependent on creater_user_test
  #---- all tests need to be indepdenent of one another. scope remains default/function

@pytest.fixture(scope="function")
def session():
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()

#!-CLIENT fixture
  # dependent on session fixture.
  # session all runs first. client is passed into all test funcs
@pytest.fixture(scope="function")
def client(session):
  def override_get_db():
    try:
      yield session
    finally:
      session.close()
  #override .database.py get_db session
  app.dependency_overrides[get_db] = override_get_db
  yield TestClient(app)


#!-TEST_USER  fixture
  #  created to uncorrelate testS by passing a new client and session in ever test
  #  test_user is created independently when called, rather than depending on success of test_create_user()
@pytest.fixture
def test_user(client):

  user_data = {"email": "hello123@gmail.com",  "password": "hello123"}
  res = client.post("/users/", json=user_data)

  new_user = res.json()
  # creater_user only returns email and id. password needs to be added manually
  new_user['password'] = user_data['password']

  assert res.status_code == 201
  return new_user


@pytest.fixture
def test_user2(client):

  user_data = {"email": "hello456@gmail.com",  "password": "hello456"}
  res = client.post("/users/", json=user_data)

  new_user = res.json()
  # creater_user only returns email and id. password needs to be added manually
  new_user['password'] = user_data['password']

  assert res.status_code == 201
  return new_user



#! TOKEN & AUTHORIZED_CLIENT fixture 
  #so test_post.py tests can authenticate 

@pytest.fixture 
def token(test_user):
  return create_access_token({"user_id": test_user['id']})

  #add token to client and update header with token 
@pytest.fixture
def authorized_client(client, token):
  client.headers = {
    **client.headers,
    "Authorization": f'Bearer {token}'
  }

  return client

#! CREATE POSTS fixture 
@pytest.fixture 
def test_posts(test_user, session, test_user2):
  posts_data = [{
    'title': '1st title',
    'content': 'first content',
    'user_id': test_user['id']
  }, {
      'title': '2nd title',
      'content': 'second content',
      'user_id': test_user['id']
  }, {
      'title': '3rd title',
      'content': 'third content',
      'user_id': test_user['id']
  }, {
      'title': 'is this working',
      'content': '2nd user content',
      'user_id': test_user2['id']
  }]

  def create_post_model(post):
    return models.Post(**post)
  
  post_map = map(create_post_model, posts_data)
  posts_list = list(post_map)

  session.add_all(posts_list)
  session.commit()

  posts_query_results = session.query(models.Post).all()
  return posts_query_results
