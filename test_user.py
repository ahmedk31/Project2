


def test_add_doctor_and_patient():
    # Setup: Empty lists simulating JSON data
    doctors = []
    patients = []

    # Test adding a doctor
    new_doctor = add_doctor(doctors, "Dr. X", "Surgeon")
    assert new_doctor in doctors, "The doctor should be added to the list"
    assert new_doctor['name'] == "Dr. X", "The doctor's name should be Dr. Test"
    assert new_doctor['specialization'] == "Surgeon", "The doctor's specialization should be General"

    # Test adding a patient
    new_patient = add_patient(patients, "Patient X", 30, "Female", "1", "101", "1B")
    assert new_patient in patients, "The patient should be added to the list"
    assert new_patient['name'] == "Patient X", "The patient's name should be Patient Test"
    assert new_patient['age'] == 30, "The patient's age should be 30"
    assert new_patient['gender'] == "Female", "The patient's gender should be Female"
    assert new_patient['doctorId'] == "1", "The patient's doctorId should be 1"
    assert new_patient['roomNumber'] == "101", "The patient's roomNumber should be 101"
    assert new_patient['bedNumber'] == "1B", "The patient's bedNumber should be 1B"

    print("All tests passed!")

# Run the test
test_add_doctor_and_patient()
