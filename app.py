from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=["*"])  # Enable CORS for all origins

# Fake symptom database - maps symptoms to conditions, advice, and urgency
# In a real application, this would be a proper database with medical data
SYMPTOM_DATABASE = {
    # Headache-related conditions
    "headache": {
        "conditions": ["Tension Headache", "Migraine", "Sinus Headache"],
        "advice": "Rest in a quiet, dark room. Stay hydrated. Consider over-the-counter pain relievers like ibuprofen or acetaminophen.",
        "urgent": False
    },
    "migraine": {
        "conditions": ["Migraine", "Cluster Headache"],
        "advice": "Lie down in a dark, quiet room. Apply cold compress to forehead. Avoid bright lights and loud noises.",
        "urgent": False
    },
    
    # Fever-related conditions
    "fever": {
        "conditions": ["Common Cold", "Flu", "COVID-19", "Bacterial Infection"],
        "advice": "Rest, stay hydrated, and monitor temperature. Take acetaminophen or ibuprofen for fever. Seek medical attention if fever persists above 103°F (39.4°C).",
        "urgent": False
    },
    "high fever": {
        "conditions": ["Severe Infection", "COVID-19", "Bacterial Infection"],
        "advice": "Seek immediate medical attention. High fever can be dangerous, especially in children and elderly.",
        "urgent": True
    },
    
    # Chest pain - always urgent
    "chest pain": {
        "conditions": ["Heart Attack", "Angina", "Pneumonia", "Costochondritis"],
        "advice": "This is a medical emergency. Call emergency services immediately. Do not drive yourself to the hospital.",
        "urgent": True
    },
    "chest tightness": {
        "conditions": ["Heart Attack", "Angina", "Anxiety", "Asthma"],
        "advice": "Seek immediate medical attention. Chest tightness can indicate serious heart or lung problems.",
        "urgent": True
    },
    
    # Respiratory symptoms
    "shortness of breath": {
        "conditions": ["Asthma", "Pneumonia", "COVID-19", "Anxiety", "Heart Problem"],
        "advice": "Seek medical attention immediately. Difficulty breathing is a serious symptom that requires prompt evaluation.",
        "urgent": True
    },
    "cough": {
        "conditions": ["Common Cold", "Flu", "COVID-19", "Bronchitis", "Pneumonia"],
        "advice": "Stay hydrated, rest, and monitor symptoms. Seek medical attention if cough is severe or accompanied by fever.",
        "urgent": False
    },
    
    # Abdominal symptoms
    "stomach pain": {
        "conditions": ["Gastritis", "Food Poisoning", "Appendicitis", "Irritable Bowel Syndrome"],
        "advice": "Rest, stay hydrated, and avoid solid foods initially. Seek medical attention if pain is severe or persistent.",
        "urgent": False
    },
    "severe abdominal pain": {
        "conditions": ["Appendicitis", "Gallbladder Disease", "Bowel Obstruction", "Kidney Stones"],
        "advice": "Seek immediate medical attention. Severe abdominal pain can indicate a serious condition requiring surgery.",
        "urgent": True
    },
    
    # Dizziness and neurological symptoms
    "dizziness": {
        "conditions": ["Vertigo", "Dehydration", "Low Blood Pressure", "Inner Ear Problem"],
        "advice": "Sit or lie down to prevent falls. Stay hydrated. Seek medical attention if dizziness is severe or accompanied by other symptoms.",
        "urgent": False
    },
    "nausea": {
        "conditions": ["Food Poisoning", "Gastritis", "Migraine", "Pregnancy", "Viral Infection"],
        "advice": "Stay hydrated with small sips of water. Rest and avoid solid foods. Seek medical attention if severe or persistent.",
        "urgent": False
    }
}

def analyze_symptoms(symptom_text):
    """
    Analyze user symptoms and return matching conditions, advice, and urgency.
    
    Args:
        symptom_text (str): User's symptom description
        
    Returns:
        dict: Contains conditions, advice, and urgent flag
    """
    # Convert to lowercase for case-insensitive matching
    symptom_text = symptom_text.lower()
    
    # Initialize response
    all_conditions = set()
    all_advice = []
    is_urgent = False
    
    # Check each symptom in our database
    for symptom, data in SYMPTOM_DATABASE.items():
        if symptom in symptom_text:
            # Add conditions to our set (prevents duplicates)
            all_conditions.update(data["conditions"])
            
            # Add advice
            all_advice.append(data["advice"])
            
            # Check if any matching symptom is urgent
            if data["urgent"]:
                is_urgent = True
    
    # If no symptoms matched, provide general advice
    if not all_conditions:
        return {
            "conditions": ["General Consultation Recommended"],
            "advice": "Your symptoms don't match our database. Please consult with a healthcare provider for proper evaluation.",
            "urgent": False
        }
    
    # Combine all advice into one comprehensive response
    combined_advice = " ".join(all_advice)
    
    return {
        "conditions": list(all_conditions),
        "advice": combined_advice,
        "urgent": is_urgent
    }

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring and testing.
    """
    return jsonify({
        "status": "healthy",
        "message": "Symptom Checker API is running",
        "version": "1.0.0"
    })

@app.route('/check-symptoms', methods=['POST'])
def check_symptoms():
    """
    Main endpoint for symptom checking.
    
    Expected input:
    {
        "input": "I have a headache and fever"
    }
    
    Returns:
    {
        "conditions": ["Tension Headache", "Common Cold"],
        "advice": "Rest in a quiet, dark room...",
        "urgent": false
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate input
        if not data or 'input' not in data:
            return jsonify({
                "error": "Missing 'input' field in request body"
            }), 400
        
        symptom_input = data['input']
        
        # Validate that input is a string
        if not isinstance(symptom_input, str):
            return jsonify({
                "error": "Input must be a string"
            }), 400
        
        # Validate that input is not empty
        if not symptom_input.strip():
            return jsonify({
                "error": "Input cannot be empty"
            }), 400
        
        # Log the request for debugging
        logger.info(f"Symptom check request: {symptom_input}")
        
        # Analyze the symptoms
        result = analyze_symptoms(symptom_input)
        
        # Log the result for debugging
        logger.info(f"Analysis result: {result}")
        
        return jsonify(result)
        
    except Exception as e:
        # Log the error for debugging
        logger.error(f"Error processing symptom check: {str(e)}")
        
        return jsonify({
            "error": "Internal server error",
            "message": "An error occurred while processing your request"
        }), 500

@app.route('/symptoms', methods=['GET'])
def get_available_symptoms():
    """
    Endpoint to get list of symptoms the system can recognize.
    Useful for frontend development and testing.
    """
    symptoms = list(SYMPTOM_DATABASE.keys())
    return jsonify({
        "symptoms": symptoms,
        "count": len(symptoms)
    })

@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors with a helpful message.
    """
    return jsonify({
        "error": "Endpoint not found",
        "message": "The requested endpoint does not exist. Available endpoints: /check-symptoms, /health, /symptoms"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """
    Handle 405 errors with a helpful message.
    """
    return jsonify({
        "error": "Method not allowed",
        "message": "This endpoint does not support the requested HTTP method"
    }), 405

if __name__ == '__main__':
    # Run the Flask app in development mode
    # In production, use a proper WSGI server like Gunicorn
    app.run(debug=True, host='0.0.0.0', port=5000) 