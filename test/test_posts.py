from app import schemas
import pytest 

#! - AUTHORIZED USER, GET ALL POSTS
def test_get_all_posts(authorized_client, test_posts):
    # authorized_client - fixture that creates & logs in a user 
    # test_posts - fixture that takes new authorized user and creates new posts
  res = authorized_client.get('/posts/')

  def validate(post):
    return schemas.PostOut(**post)

  posts_map = map(validate, res.json())
  posts_list = list(posts_map)

  #print(res.json())
  assert len(res.json()) == len(test_posts)
  assert res.status_code == 200

#! - UN_AUTHORIZED USER, GET ALL POSTS 
def test_unauthorized_user_get_all_posts(client, test_posts):
  res = client.get('/posts/')
  assert res.status_code == 401

#! - UN_AUTHORIZED USER, GET POST BY ID 
def test_unauthorized_user_get_one_post(client, test_posts):
  res = client.get(f'/posts/{test_posts[0].id}')
  assert res.status_code == 401

#! - AUTHORIZED USER, GET POST BY NON EXISTANT ID
def test_get_one_post_not_exists(authorized_client, test_posts):
  res = authorized_client.get(f'/posts/88888')
  assert res.status_code == 404

#! - AUTHORORIZED USER, GET POST BY EXISTING ID
def test_get_one_post(authorized_client, test_posts):
  res = authorized_client.get(f'/posts/{test_posts[0].id}')

  post = schemas.PostOut(**res.json()) #spread into pydantic model 
  assert post.Post.id == test_posts[0].id
  assert post.Post.content == test_posts[0].content 
  assert post.Post.title == test_posts[0].title

#!- AUTHORIZED USER - CREATE NEW POSTS 
@pytest.mark.parametrize("title, content, published", [
  ("awesome new title", "awesome new content", True),
  ("pizza time", "mushroom pepperoni", False),
  ("just woke up", "look at me", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
  res = authorized_client.post('/posts/',
    json = {"title": title, "content": content, "published": published})

  created_post = schemas.Post(**res.json())

  assert res.status_code == 201
  assert created_post.title == title 
  assert created_post.content == content
  assert created_post.title == title
  assert created_post.published == published
  assert created_post.user_id == test_user['id']

#!- AUTHORIZED USER - CREATE POST & DEFAULT PUBLISHED VALUE IS TRUE
@pytest.mark.parametrize("title, content", [
    ("new title", "awesome new content"),
    ("bagel time", "mushroom pepperoni"),
    ("just got up", "look at me")
])
def test_create_post_default_published_true(authorized_client, test_user, test_posts, title, content):
  res = authorized_client.post('/posts/', json={"title": title, "content": content})

  created_post = schemas.Post(**res.json())

  assert res.status_code == 201
  assert created_post.title == title
  assert created_post.content == content
  assert created_post.published == True
  assert created_post.user_id == test_user['id']


#! UN_ATHORIZED USER - CREATE POST 
@pytest.mark.parametrize("title, content, published", [
    ("new title", "awesome new content", True)
])
def test_unauthorized_user_create_post(client, test_user, test_posts, title, content, published):
  res = client.post(
      '/posts/', json={"title": title, "content": content, "published": published})

  assert res.status_code == 401

#! UN_ATHORIZED USER - DELETE POST
def test_unauthorized_user_delete_post(client, test_user, test_posts):
  res = client.delete(f'/posts/{test_posts[0].id}')
  assert res.status_code == 401

#! ATHORIZED USER - DELETE POST
def test_authorized_user_delete_post(authorized_client, test_user, test_posts):
  res = authorized_client.delete(f'/posts/{test_posts[0].id}')
  assert res.status_code == 204

#! ATHORIZED USER - DELETE NON EXISTANT POST 
def test_authorized_user_delete_post_not_exists(authorized_client, test_user, test_posts):
  res = authorized_client.delete(f'/posts/9999999')
  assert res.status_code == 404

#! ATHORIZED USER - DELETE POST BELONING TO OTHER USER
def test_authorized_user_delete_other_users_post(authorized_client, test_user, test_user2, test_posts):
  #authorized_client is _always_ logged in as test_user. 
  #test_user2 has a post but is not logged in
  res = authorized_client.delete(f'/posts/{test_posts[3].id}')
  assert res.status_code == 403

#!- AUTHORIZED USER - UPDATE OWN POST
def test_authorized_user_update_post(authorized_client, test_user, test_posts):

  data = {
    "title": "updated title",
    "content": "updated contents about new content",
    "id": test_posts[0].id
  }

  res = authorized_client.put(f'/posts/{test_posts[0].id}', json=data)

  updated_post = schemas.Post(**res.json())

  assert res.status_code == 202
  assert updated_post.title == data["title"]
  assert updated_post.content == data["content"]

#!- AUTHORIZED USER - UPDATE OTHER USERS POST
def test_authorized_user_update_post(authorized_client, test_user, test_user2, test_posts):

  data = {
      "title": "updated title",
      "content": "updated contents about new content",
      "id": test_posts[3].id
  }

  res = authorized_client.put(f'/posts/{test_posts[3].id}', json=data)
  assert res.status_code == 403

#!- UN_AUTHORIZED USER - UPDATE POST
def test_unauthorized_user_update_post(client, test_user, test_posts):

  data = {
      "title": "updated title",
      "content": "updated contents about new content",
      "id": test_posts[0].id
  }

  res = client.put(f'/posts/{test_posts[3].id}', json=data)
  assert res.status_code == 401

#! AUTHORIZED USER - UPDATE NON EXISTANT POST
def test_authorized_user_update_post_not_exists(authorized_client, test_user, test_posts):
  data = {
      "title": "updated title",
      "content": "updated contents about new content",
      "id": test_posts[0].id
  }
  res = authorized_client.put(f'/posts/9999999', json = data)
  assert res.status_code == 404
