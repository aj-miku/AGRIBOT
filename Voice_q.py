import subprocess
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

cred = credentials.Certificate("agribot-6a797-firebase-adminsdk-8c8qp-55d4d018dc.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def read_sample_data(filename):
    sample_data = {}
    with open(filename, "r") as file:
        for line in file:
            question, answer = line.strip().split("|")
            sample_data[question.casefold()] = answer  # Store casefolded version of question
    return sample_data

def get_field_condition():
    doc_ref = db.collection("AgriBot").document("AgriBotDataUpdate1")
    doc = doc_ref.get()
    if doc.exists:
        field_data = doc.to_dict()
        if not field_data.get('Crops', ''):
            return "No harvestable crops available for the Season"
        else:
            return f"Your Field Condition:\nYou can harvest {field_data.get('Crops', '')},\n It will take {field_data.get('Days to Maturity', '')} to Mature,\nThe Humidity is {field_data.get('Humidity (%)', '')},\nIndia Growing Season of {field_data.get('Crops', '')} is {field_data.get('India Growing Season', '')},\nPH Value is {field_data.get('PH Value', '')},\nThe Moisture in soil is {field_data.get('Soil Moisture (%)', '')},\nTodays Temperature is {field_data.get('Temperature(in Cel)', '')} celsius"
    else:
        return "Field condition data not available."

def get_answer(question, sample_data):
    question_casefolded = question.casefold()  # Convert question to casefolded version
    if question_casefolded in sample_data:
        return sample_data[question_casefolded]
    elif question_casefolded == "what is my field condition?" or question_casefolded == "what is my field condition":
        return get_field_condition()
    elif question_casefolded == "what crop can i harvest this season?" or question_casefolded == "what crop can i harvest this season":
        doc_ref = db.collection("AgriBot").document("AgriBotDataUpdate1")
        doc = doc_ref.get()
        if doc.exists:
            field_data = doc.to_dict()
            return f"You can harvest the {field_data.get('Crops', '')} for this season of the month {datetime.now().strftime('%B')}"
        else:
            return "Field condition data not available."
    else:
        return "Answer not available for this question."

def receive_and_send_data():
    # Example: Receive data from Firestore
    collection_ref = db.collection("AgriBot")
    doc_ref = collection_ref.document("Questions")
    doc = doc_ref.get()
    if doc.exists:
        received_question = doc.to_dict()["Question"]
    else:
        received_question = "No question found in Firestore"

    # Read question-answer pairs from the text file
    sample_data = read_sample_data("VoiceQuest.txt")

    # Get the answer based on the received question
    answer = get_answer(received_question, sample_data)

    # Update the Firestore database with the answer
    document_id = "Answer"
    doc_ref = db.collection("AgriBot").document(document_id)
    doc_ref.set({"Question": received_question, "Answer": answer})

    print("Data sent to Firestore successfully.")

# Automatically run other Python files if specific questions are asked
def run_other_scripts_if_needed(question):
    if question.casefold() in ["what is my field condition?", "what crop can i harvest this season?","what is my field condition","what crop can i harvest this season"]:
        subprocess.run(["python", "FirebaseGetValues.py"])
        subprocess.run(["python", "ProcessData.py"])
        subprocess.run(["python", "FirebaseUpdateData.py"])

if __name__ == "__main__":
    # Run your main function
    collection_ref = db.collection("AgriBot")
    doc_ref = collection_ref.document("Questions")
    doc = doc_ref.get()
    if doc.exists:
        received_question = doc.to_dict()["Question"]
    else:
        received_question = "No question found in Firestore"

    run_other_scripts_if_needed(received_question)
    receive_and_send_data()
