# Project2
Healthcare Database

## Introduction
This application is a medical record management system designed to securely manage and provide access to patient and doctor data. It allows patients to view their medical records and notes from their doctors, while enabling doctors to access patient information relevant to their care.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Documentation](#documentation)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Testing](#testing)
- [Contributors](#contributors)
- [License](#license)

## Installation
Follow these steps to set up the application:
1. Clone the repository:
    `git clone https://github.com/ahmedk31/Project2.git`
2. Install necessary dependencies:
    `pip install -r requirements.txt`
3. Start the application:
    `python run.py`

## Usage
- **Doctors**: View and manage patient profiles, including medical records and notes.
- **Patients**: Access their own medical information and notes from their doctors.

## Features
- Secure patient and doctor data management.
- Access control tailored for different user roles.

## Dependencies
Dependencies are listed in the `requirements.txt` file, necessary for running the application.

## Documentation
Further documentation provides deeper insights into each module's functionalities.

## API Documentation


### User Management

#### Register User
- **Endpoint:** `POST /register`
- **Description:** Registers a new user as either a doctor or a patient.
- **Payload:**
  ```json
  {
    "username": "user1",
    "email": "user@example.com",
    "password": "securepassword",
    "role": "doctor"
  }
- **Response:** Returns the newly created users's ID, name, and specialization.
- **Status Codes:**
  - `201 Created` if the user is successfully created.
  - `400 Bad Request` if required fields are missing or invalid.

### Doctor Endpoints

#### Add a Doctor
- **Endpoint:** `POST /doctors`
- **Description:** Adds a new doctor to the system.
- **Payload:**
  ```json
  [{
    "name": "Doctor Name",
    "specialization": "Specialization"
  }]


- **Response:** Returns the newly created doctor's ID, name, and specialization.
- **Status Codes:**
  - `201 Created` if the doctor is successfully created.
  - `400 Bad Request` if the name or specialization is missing.

#### Get All Doctors
- **Endpoint:** `GET /doctors`
- **Description:** Retrieves a list of all doctors in the system.
- **Response:**
  ```json
  [{
    "id": 1,
    "name": "Doctor Name",
    "specialization": "Specialization"
  }]


- **Status Codes:**
    -`200 OK` on successful retrival

### Patient Endpoints
#### Add a Patient
- **Endpoint:** `POST /patients`
- **Description:** Adds a new patient to the system.

- **Payload:**
  ```json
    [{  
    "name": "Patient Name",
    "age": 25,
    "gender": "Gender",
    "doctor_id": 1,
    "room_number": "Room Number",
    "bed_number": "Bed Number"
    }]

- **Response:** Returns the newly created patient's ID and name
- **Status Codes:**
    -`201 Created` if the patient is successfully created
    -`400 Bad Request` if any required data is missing

## Get All Patients

- **Endpoint:** `GET /patients`
- **Description:** Retrieves a list of all patients in the system.
- **Response:**
  ```json
  [{
    "id": pat.id,
    "name": pat.name,
    "age": pat.age,
    "gender": pat.gender,
    "doctor_id": pat.doctor_id
  } for pat in patients]

- **Status Codes:**
    -`200 OK` on successful retrival.

### Check History
#### Add Check History
- **Endpoint:** `POST /Check History`
- **Description:** Records a new check-up event for a patient.
- **Payload**:
  ```json
  [{
     "patient_id": 123,
    "check_time": "2023-09-01T14:00:00Z"
  }]

- **Response:** Returns the ID of the newly created check history record
- **Status Codes:**
    -`201 Created` if the check history is successfully created

## Database Schema

### Models

#### User
- **id**: Primary key
- **role**: String (choices: Doctor or Patient)
- **username**: String (Unique, Not Null)
- **email**: String (Unique, Not Null)
- **password_hash**: String

#### Doctor
- **id**: Primary key
- **name**: String (Not Null)
- **specialization**: String (Not Null)
- **patients**: Relationship (defines the association with patients)

#### Patient
- **id**: Primary key
- **name**: String (Not Null)
- **age**: Integer
- **gender**: String
- **doctor_id**: ForeignKey (references Doctor)
- **room_number**: String
- **bed_number**: String
- **diagnosis**: String
- **prescribed_medicine**: String

#### CheckHistory
- **id**: Primary key
- **patient_id**: ForeignKey (references Patient)
- **check_time**: DateTime (default is current UTC time)

### Testing

Testing ensures application reliability and verifies that all components of the database interact correctly and maintain integrity under various conditions.


- **Models:**
```bash
    pytest test_models.py
```
- **Routes:**
```bash
    pytest test_routes.py
```

## Contributors

Kawar Ahmed


