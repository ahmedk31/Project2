from app import create_app

class TestFlaskApi:
    def setup_method(self, method):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_doctor(self):
        response = self.client.post('/doctors', json={
            'name': 'John Doe',
            'specialization': 'Cardiology'
        })
        assert response.status_code == 201, "Failed to create a new doctor"

    def test_list_doctors(self):
        response = self.client.get('/doctors')
        assert response.status_code == 200, "Failed to fetch the list of doctors"

    def test_create_patient(self):
        response = self.client.post('/patients', json={
            'name': 'Alice Smith',
            'age': 30,
            'gender': 'Female',
            'doctor_id': 'doctor123',
            'room_number': 101,
            'bed_number': 1
        })
        assert response.status_code == 201, "Failed to create a new patient"
