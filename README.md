# Healthcare Database Management System

## Introduction
This Flask-based application is designed to manage healthcare data securely, providing functionalities for both doctors and patients to access and manage their respective information. It supports asynchronous background tasks for efficient data processing and includes extensive API endpoints for comprehensive interaction with the system.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Background Tasks](#background-tasks)
- [Dependencies](#dependencies)
- [Testing](#testing)
- [Contributors](#contributors)
- [License](#license)

## Installation
To set up this project locally, follow these steps:
1. Clone the repository:
    ```bash
    git clone https://github.com/ahmedk31/Project2.git
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the application:
    ```bash
    python run.py
    ```

## Usage
This application provides separate interfaces for doctors and patients:
- **Doctors**: Can add patient records, update medical histories, and access patient information.
- **Patients**: Can view their medical histories and update their personal information.

## Features
- Secure management of patient and doctor data.
- Asynchronous task processing for operations that require extensive processing time.
- Comprehensive RESTful API providing access to all functionalities of the system.

## API Documentation
The system includes the following endpoints grouped by functionality:

### User Management
- **Register User**: `POST /register`
- **Login User**: `POST /login`

### Doctor Endpoints
- **Add Doctor**: `POST /doctors`
- **List Doctors**: `GET /doctors`

### Patient Endpoints
- **Add Patient**: `POST /patients`
- **List Patients**: `GET /patients`

### Medical Records
- **Add Record**: `POST /check_history`
- **Update Patient Info**: `POST /update_patient/<int:patient_id>`

## Database Schema
### Models
#### User
- `id`: Integer, Primary Key
- `username`: String, Unique, Not Null
- `email`: String, Unique, Not Null
- `password_hash`: String

#### Doctor
- `id`: Integer, Primary Key
- `name`: String, Not Null
- `specialization`: String

#### Patient
- `id`: Integer, Primary Key
- `name`: String, Not Null
- `age`: Integer
- `gender`: String
- `doctor_id`: ForeignKey, References Doctor.id

#### CheckHistory
- `id`: Integer, Primary Key
- `patient_id`: ForeignKey, References Patient.id
- `check_time`: DateTime, Default is current UTC time

## Background Tasks
This system uses background tasks for sending email notifications and processing data updates. These tasks are managed through a queue system where tasks are added and processed asynchronously.

## Dependencies
The application requires several Python libraries, detailed in the `requirements.txt` file, including Flask, SQLAlchemy, pytest, and bcrypt.

## Testing
Tests are written for models, routes, and background tasks:
- **Models**: `pytest test_models.py`
- **Routes**: `pytest test_routes.py`
- **Background Tasks**: `pytest test_background_tasks.py`

## Contributors
- Kawsar Ahmed