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

def background_worker(app):
    with app.app_context():
        while True:
            task = task_queue.get()
            if task is None:  # Stop signal
                break
            update_patient_record(task['patient_id'], task['updates'])
            task_queue.task_done()


worker_thread = None

def start_worker(app):
    global worker_thread
    if worker_thread is None or not worker_thread.is_alive():
        worker_thread = threading.Thread(target=background_worker, args=(app,), daemon=True)
        worker_thread.start()

def stop_worker():
    global worker_thread
    if worker_thread and worker_thread.is_alive():
        task_queue.put(None)
        worker_thread.join()
        worker_thread = None