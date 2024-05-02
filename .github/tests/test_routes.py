from app import create_app

def test_home_page():
    app = create_app('config.TestingConfig')
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data  # Adjust according to your actual home page response

def test_add_doctor():
    app = create_app('config.TestingConfig')
    client = app.test_client()
    response = client.post('/add_doctor', json={
        'email': 'doc@example.com',
        'first_name': 'Doc',
        'last_name': 'Holiday',
        'password': 'verysecure',
        'specialization': 'Dentistry'
    })
    assert response.status_code == 201
    assert b"Doctor added successfully" in response.data

def test_add_patient():
    app = create_app('config.TestingConfig')
    client = app.test_client()
    response = client.post('/add_patient', json={
        'email': 'patient@example.com',
        'first_name': 'Pat',
        'last_name': 'Smith',
        'password': 'securepassword',
        'age': 30,
        'gender': 'Female',
        'doctor_id': 'some_doctor_id'
    })
    assert response.status_code == 201
    assert b"Patient added successfully" in response.data
