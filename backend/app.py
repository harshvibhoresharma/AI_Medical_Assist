from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import threading
import requests

# --- Initialization ---
app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing

# --- In-Memory Data Store ---
# Using a simple list and dictionary for the queue and patient data
# In a production environment, this would be a database (e.g., PostgreSQL, MongoDB)
patient_queue = []
patient_details = {}
next_patient_id = 1
queue_lock = threading.Lock() # To handle concurrent requests safely

# --- Load ML Model ---
try:
    model = joblib.load('triage_model.pkl')
    mlb = joblib.load('mlb.pkl')
    print("✅ Model and binarizer loaded successfully.")
except FileNotFoundError:
    print("🔴 ERROR: Model files not found. Please run 'model_trainer.py' first.")
    exit()

# --- Utility Functions ---
def get_priority_details(score):
    """Assigns a priority level and color based on the score."""
    if score > 85:
        return {"level": "Critical", "cssClass": "priority-critical"}
    if score > 60:
        return {"level": "High", "cssClass": "priority-high"}
    if score > 30:
        return {"level": "Medium", "cssClass": "priority-medium"}
    return {"level": "Low", "cssClass": "priority-low"}

def send_doctor_alert(patient):
    """(Bonus Feature) Sends a notification for critical patients using a free webhook service."""
    if patient['priority']['level'] in ["Critical", "High"]:
        try:
            # Using ntfy.sh - a free, no-signup-required pub-sub notification service
            # Replace 'your-hackathon-hospital-alerts' with a unique topic name
            topic = "ai-triage-system-critical-alerts"
            title = f"🚨 {patient['priority']['level']} Priority Alert"
            message = f"Patient {patient['name']} (ID: {patient['id']}) requires immediate attention. Score: {patient['score']}"
            
            # This sends a POST request to the ntfy.sh topic.
            # Anyone subscribed to https://ntfy.sh/your-hackathon-hospital-alerts will get the notification.
            requests.post(
                f"https://ntfy.sh/{topic}",
                data=message.encode('utf-8'),
                headers={"Title": title, "Priority": "high"}
            )
            print(f"✉️ Alert sent for critical patient: {patient['name']}")
        except Exception as e:
            print(f"🔴 Failed to send alert: {e}")


# --- API Endpoints ---
@app.route('/triage', methods=['POST'])
def triage_patient():
    """
    Receives patient data, predicts priority, and adds them to the queue.
    """
    global next_patient_id
    data = request.json
    
    if not data or 'name' not in data or 'symptoms' not in data:
        return jsonify({"error": "Invalid input data"}), 400

    symptoms = data['symptoms']
    
    # Preprocess symptoms for the model
    try:
        input_vector = mlb.transform([symptoms])
    except ValueError as e:
        # This can happen if a symptom is not in the binarizer's list of classes
        return jsonify({"error": f"Invalid symptom found: {e}"}), 400

    # Predict probabilities and calculate a weighted score
    probabilities = model.predict_proba(input_vector)[0]
    # Weights for [Low, Medium, High, Critical] priorities
    score = np.dot(probabilities, [10, 40, 75, 100])

    with queue_lock:
        new_patient = {
            "id": next_patient_id,
            "name": data['name'],
            "score": f"{score:.2f}",
            "priority": get_priority_details(score),
            "symptoms": symptoms
        }
        
        patient_details[next_patient_id] = new_patient
        
        # Add patient ID to the queue and sort by score
        patient_queue.append(next_patient_id)
        patient_queue.sort(key=lambda pid: float(patient_details[pid]['score']), reverse=True)
        
        next_patient_id += 1
        
        # (Bonus) Send an alert if patient is critical
        send_doctor_alert(new_patient)

    return jsonify({"message": "Patient added to queue", "patient": new_patient}), 201


@app.route('/queue', methods=['GET'])
def get_queue():
    """
    Returns the current state of the patient queue.
    """
    with queue_lock:
        # Create a list of patient objects from the IDs in the queue
        ordered_patients = [patient_details[pid] for pid in patient_queue]
    return jsonify(ordered_patients)


@app.route('/patient/next', methods=['POST'])
def get_next_patient():
    """
    Removes the highest-priority patient from the queue and returns them.
    """
    with queue_lock:
        if not patient_queue:
            return jsonify({"message": "Queue is empty"}), 404
        
        next_patient_id = patient_queue.pop(0) # Remove the first patient (highest score)
        attended_patient = patient_details.pop(next_patient_id)
        
    return jsonify(attended_patient)


if __name__ == '__main__':
    # Use 0.0.0.0 to make it accessible on your local network
    app.run(host='0.0.0.0', port=5001, debug=True)
