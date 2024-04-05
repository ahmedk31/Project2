def add_doctor(doctors, name, specialization):
    new_id = str(len(doctors) + 1)
    new_doctor = {
        "id": new_id,
        "name": name,
        "specialization": specialization
    }
    doctors.append(new_doctor)
    return new_doctor

def add_patient(patients, name, age, gender, doctor_id, room_number, bed_number):
    new_id = str(len(patients) + 1)
    new_patient = {
        "id": new_id,
        "name": name,
        "age": age,
        "gender": gender,
        "doctorId": doctor_id,
        "roomNumber": room_number,
        "bedNumber": bed_number
    }
    patients.append(new_patient)
    return new_patient
