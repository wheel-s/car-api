

def test_user_create(db_session, test_user):
    assert test_user.id is not None
    assert test_user.email == "test@example.com"


# def test_auth(client, auth_headers):
#     response = client.get("/users/me",
#                           headers=auth_headers)
    
#     assert response.status_code == 200

#     data = response.json()
#     token = data["access_token"]
#     print(data)
#     return {"Authorization":f"Bearer {token}"}