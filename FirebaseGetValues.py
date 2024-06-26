import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

try:
    app = firebase_admin.get_app(name="myApp")
except ValueError:
    cred = credentials.Certificate("agribot-6a797-firebase-adminsdk-8c8qp-55d4d018dc.json")
    app = firebase_admin.initialize_app(cred, name="myApp")

db = firestore.client(app=app)
document_id = "AgriBotDataUpdate"
doc_ref = db.collection("AgriBot").document(document_id)
doc = doc_ref.get()

if doc.exists:
    data = doc.to_dict()
    humidity_str = data.get("Humidity", "")
    temperature_str = data.get("Temperature", "")
    ph_str = data.get("Ph", "")
    moisture_str = data.get("Moisture", "")

    try:
        humidity = float(humidity_str)
        temperature = float(temperature_str)
        ph = float(ph_str)
        moisture = abs(float(moisture_str))
        # print(f"Humidity: {humidity}")
        # print(f"Temperature: {temperature}")
        # print(f"Ph: {ph}")
        # print(f"Moisture: {moisture}")
    except ValueError:
        print("Error: Unable to convert string values to floats.")
else:
    print("Document does not exist.")
