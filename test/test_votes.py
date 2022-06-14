import pytest 
from app import models 

@pytest.fixture()
def test_vote(test_posts, session, test_user):
  new_vote = models.Vote(post_id = test_posts[3].id, user_id = test_user['id'])
  session.add(new_vote)
  session.commit()

#!- VOTE ON A POST
def test_vote_on_post(authorized_client, test_posts):
  res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})

  assert res.status_code == 201

#! - VOTE ON A VOTE TWICE
def test_vote_twice_post(authorized_client, test_posts, test_vote):
  res = authorized_client.post('/vote/', json = {"post_id": test_posts[3].id, "dir": 1})

  assert res.status_code == 409

#! - DELETE A EXISTING VOTE
def test_delete_vote_exists(authorized_client, test_posts, test_vote):
  res = authorized_client.post(
      "/vote/", json={"post_id": test_posts[3].id, "dir": 0})

  assert res.status_code == 201

#! - DELETE A NON-EXISTING VOTE - test_vote fixture not included
def test_delete_vote_not_exists(authorized_client, test_posts):
  res = authorized_client.post(
      "/vote/", json={"post_id": test_posts[3].id, "dir": 0})

  assert res.status_code == 404

#! - VOTE FOR A NON-EXISTING POST
def test_vote_post_not_exists(authorized_client, test_posts):
  res = authorized_client.post(
      "/vote/", json={"post_id": 9999999, "dir": 1})

  assert res.status_code == 404


#! - NON AUTHORIZED USER VOTE
def test_vote_unauthorized_user(client, test_posts):
  res = client.post(
      "/vote/", json={"post_id": test_posts[3].id, "dir": 1})

  assert res.status_code == 401
