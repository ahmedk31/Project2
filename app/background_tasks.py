import queue
import logging
import threading
from threading import Event
from flask import current_app
from .database import db
from .models import Patient

task_queue = queue.Queue()

logging.basicConfig(level=logging.DEBUG)

#This function will probably be moved later, should 
def update_patient_record(patient_id, updates): 
    with current_app.app_context():
        patient = db.session.get(Patient, patient_id)
        if patient:
            for key, value in updates.items():
                setattr(patient, key, value)
            db.session.commit()

def background_worker(app):
    with app.app_context():
        while True:
            task = task_queue.get()
            if task is None:
                break
            logging.debug(f"Processing task for patient {task['patient_id']}")
            update_patient_record(task['patient_id'], task['updates'])
            if 'event' in task:
                task['event'].set()
            task_queue.task_done()

worker_thread = None

def start_worker(app):
    global worker_thread
    if worker_thread is None or not worker_thread.is_alive():
        worker_thread = threading.Thread(target=background_worker, args=(app,), daemon=True)
        worker_thread.start()

def stop_worker():
    global worker_thread
    if worker_thread is not None:
        task_queue.put(None)  # Signal the worker thread to terminate
        if worker_thread.ident != threading.get_ident():
            worker_thread.join()  # Only join if not the current thread
        worker_thread = None