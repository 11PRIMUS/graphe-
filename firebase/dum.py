import firebase_admin
from firebase_admin import credentials, db

cred=credentials.Certificate(r"C:\pro\suryamukhii\scripts\surya-mukhi-firebase-adminsdk-35jq9-f3122bd9fb.json")
firebase_admin.initialize_app(cred,{
    "databaseURL": "https://surya-mukhi-default-rtdb.asia-southeast1.firebasedatabase.app"})

dummy_data = {
    "WeatherData1": {
        "-Nx1": {"temperature": 22.5, "timestamp": 1713754800000},
        "-Nx2": {"temperature": 23.1, "timestamp": 1713758400000},
        "-Nx3": {"temperature": 24.8, "timestamp": 1713762000000},
        "-Nx4": {"temperature": 26.3, "timestamp": 1713765600000},
        "-Nx5": {"temperature": 28.7, "timestamp": 1713769200000},
        "-Nx6": {"temperature": 30.2, "timestamp": 1713772800000},
        "-Nx7": {"temperature": 31.5, "timestamp": 1713776400000},
        "-Nx8": {"temperature": 32.0, "timestamp": 1713780000000},
        "-Nx9": {"temperature": 31.2, "timestamp": 1713783600000},
        "-Nx10": {"temperature": 29.8, "timestamp": 1713787200000},
        "-Nx11": {"temperature": 27.4, "timestamp": 1713790800000},
        "-Nx12": {"temperature": 25.9, "timestamp": 1713794400000}
    }
}
def send_dum():
    try:
        dum_ref=db.reference("WeatherData1")
        for key, value in dummy_data["WeatherData1"].items():
            dum_ref.child(key).set(value)  
        print("Dummy data sent to Firebase")
    except Exception as e:
        print(f"Error sending data to Firebase: {e}")

if __name__ == "__main__":
    send_dum()

