import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MultiLabelBinarizer
import joblib
import numpy as np

# --- 1. Define Symptoms (Features) ---
# This list MUST match the one in the frontend.
SYMPTOMS = [
    "Fever", "Cough", "Shortness of Breath", "Chest Pain", "Headache",
    "Abdominal Pain", "Nausea", "Vomiting", "Dizziness", "Fatigue",
    "Severe Bleeding", "Loss of Consciousness", "Seizure", "Major Trauma",
    "High Blood Pressure", "Stroke Symptoms", "Allergic Reaction"
]

# --- 2. Generate Synthetic Training Data ---
# In a real-world scenario, this would be historical patient data.
data = {
    'symptoms': [
        ['Chest Pain', 'Shortness of Breath', 'Dizziness'],
        ['Severe Bleeding', 'Major Trauma'],
        ['Loss of Consciousness', 'Seizure'],
        ['Stroke Symptoms', 'High Blood Pressure', 'Headache'],
        ['Cough', 'Fever', 'Headache'],
        ['Abdominal Pain', 'Nausea', 'Vomiting'],
        ['Allergic Reaction', 'Shortness of Breath'],
        ['Fatigue', 'Dizziness'],
        ['Fever', 'Cough'],
        ['Headache'],
        ['High Blood Pressure'],
        ['Chest Pain', 'Nausea'],
        ['Major Trauma', 'Shortness of Breath'],
        ['Seizure'],
        ['Vomiting', 'Fever'],
        ['Stroke Symptoms', 'Dizziness']
    ],
    # Priority Levels: 3=Critical, 2=High, 1=Medium, 0=Low
    'priority': [3, 3, 3, 3, 1, 1, 2, 0, 0, 0, 1, 2, 3, 3, 1, 3]
}
df = pd.DataFrame(data)

# --- 3. Preprocess the Data ---
# Convert list of symptoms into a binary matrix (one-hot encoding)
mlb = MultiLabelBinarizer(classes=SYMPTOMS)
X = mlb.fit_transform(df['symptoms'])
y = df['priority']

print("--- Feature Matrix (X): ---")
print(pd.DataFrame(X, columns=mlb.classes_).head())
print("\n--- Target Vector (y): ---")
print(y.head())

# --- 4. Train the Model ---
# Splitting data is best practice, but with this tiny dataset, we'll train on all of it.
# For a real project, you would use: X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X, y)

print(f"\nModel trained successfully on {len(df)} records.")
print(f"Model Accuracy (on training data): {model.score(X, y):.2f}")

# --- 5. Save the Model and the Binarizer ---
# We need to save the binarizer to process new, incoming data in the same way.
joblib.dump(model, 'triage_model.pkl')
joblib.dump(mlb, 'mlb.pkl')

print("\nModel saved as 'triage_model.pkl'")
print("Binarizer saved as 'mlb.pkl'")

# --- 6. Example Prediction ---
def predict_priority(symptoms_list):
    """Function to test the saved model."""
    loaded_model = joblib.load('triage_model.pkl')
    loaded_mlb = joblib.load('mlb.pkl')
    
    # Transform input using the loaded binarizer
    input_data = loaded_mlb.transform([symptoms_list])
    
    # Predict probability for each class
    probabilities = loaded_model.predict_proba(input_data)[0]
    
    # Create a weighted score. We give higher weight to higher priority classes.
    # Weights for [Low, Medium, High, Critical]
    score = np.dot(probabilities, [10, 40, 75, 100])
    
    predicted_class = loaded_model.predict(input_data)[0]
    
    return predicted_class, score, probabilities

print("\n--- Example Prediction Test ---")
test_symptoms = ['Cough', 'Fever', 'Shortness of Breath']
predicted_class, score, probabilities = predict_priority(test_symptoms)
print(f"Symptoms: {test_symptoms}")
print(f"Predicted Priority Class: {predicted_class} (0:Low, 1:Medium, 2:High, 3:Critical)")
print(f"Calculated Urgency Score: {score:.2f}")
print(f"Class Probabilities [0, 1, 2, 3]: {probabilities}")
