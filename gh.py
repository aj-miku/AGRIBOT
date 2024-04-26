import subprocess
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("agribot-6a797-firebase-adminsdk-8c8qp-55d4d018dc.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def run_voice_q_script():
    subprocess.run(["python", "-c", f"import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/dark-d07/AgriBot/main/Voice_q.py').read())"]) # Replace "path/to/your/Voice_q.py" with the actual path

# def get_answer_from_firestore(question):
#     try:
#         doc_ref = db.collection("AgriBot").document("Answer")
#         doc = doc_ref.get()
#         return doc.to_dict().get()
#     except Exception as e:
#         return f"Error retrieving answer: {str(e)}"

if __name__ == "__main__":
    # question = input("Ask a question: ")
    # document_id = "Questions"
    # doc_ref = db.collection("AgriBot").document(document_id)
    # doc_ref.set({"Question": question})
    run_voice_q_script()
    # document_id = "Answer"
    # doc_ref1 = db.collection("AgriBot").document(document_id)
    # answer=doc_ref1.get()
    # answer = answer.to_dict()["Answer"]
    # print(answer)