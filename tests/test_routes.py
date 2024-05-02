import pytest
from app import create_app, db
from app.models import Doctor

@pytest.fixture
def app():
    app = create_app('Config')
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_add_doctor(client):
    response = client.post('/add_doctor', json={'name': 'Dr. House', 'specialization': 'Diagnostic Medicine'})
    assert response.status_code == 200
    assert response.json['name'] == 'Dr. House'
