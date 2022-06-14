from app import schemas 
from jose import jwt 
from app.config import settings
import pytest 

# TEST 0 - url:port/
# def test_root(client):
#   res = client.get("/")
#   print(res.json().get('message'))
#   assert res.json().get('message') == "Hello World. Is there anyone out there?"
#   assert res.status_code == 200
#   # return {"message": "Hello World. Is there anyone out there?"}


#! test_create_user
  # alternative: skip the test entirely with decorator
  # @pytest.mark.skip(reason="user already successfully created")

def test_create_user(client):
  res = client.post("/users/", json = {"email":"hello123@gmail.com", "password":"hello123"})
  # trailing slash added to /users because fastapi will redirect/http code 307 to /users/. 
  # assertion will fail without the trailing slash because 307 != 201
  new_user = schemas.UserOut(**res.json())
  assert new_user.email == "hello123@gmail.com"
  assert res.status_code == 201

#! test_login_user 
  # log in & validate access token
def test_login_user(client, test_user):

  res = client.post("/login",
    data = {"username": test_user['email'], "password": test_user['password']})

  #unpack the access token
  login_res = schemas.Token(**res.json())

  #decode token and get user id
  payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
  id = payload.get("user_id")

  # validate that id in decoded token matches test_user's id
  assert id == test_user['id']
  assert login_res.token_type == 'bearer'
  assert res.status_code == 200

#! TEST_INCORRECT_LOGIN 
  # validate response from failed login attempt 

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'hello123', 403),
    ('hello123@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'hello123', 422),
    ('hello123@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
  res = client.post("/login",
                    data={"username": email, "password": password})

  assert res.status_code == status_code
  #assert res.json().get('detail') == 'Invalid Credentials'
