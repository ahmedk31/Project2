from app import create_app, db

def test_register():
    app = create_app('TestConfig')
    client = app.test_client()
    response = client.post('/register', json={
        'email': 'user@example.com',
        'username': 'user1',
        'password': 'securepassword123'
    })
    assert response.status_code == 201
    assert b"user1" in response.data

def test_doctors_list():
    app = create_app('TestConfig')
    client = app.test_client()
    response = client.get('/doctors')
    assert response.status_code == 200
    assert b"[]" in response.data  # Expecting an empty list initially
