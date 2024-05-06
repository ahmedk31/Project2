import queue
import threading
from flask import current_app
from .database import db
from .models import Patient

task_queue = queue.Queue()

def update_patient_record(patient_id, updates):
    with current_app.app_context():
        patient = Patient.query.get(patient_id)
        if patient:
            for key, value in updates.items():
                setattr(patient, key, value)
            db.session.commit()

def background_worker():
    while True:
        task = task_queue.get()
        if task is None:  # Stop signal
            break
        update_patient_record(task['patient_id'], task['updates'])
        task_queue.task_done()

worker_thread = threading.Thread(target=background_worker)
worker_thread.daemon = True

def start_worker():
    if not worker_thread.is_alive():
        worker_thread.start()

def stop_worker():
    if worker_thread.is_alive():
        task_queue.put(None)
        worker_thread.join()
