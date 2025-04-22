import firebase_admin
from firebase_admin import credentials, db

cred=credentials.Certificate(r"C:\pro\suryamukhii\scripts\surya-mukhi-firebase-adminsdk-35jq9-f3122bd9fb.json")
firebase_admin.initialize_app(cred,{
    "databaseURL": "https://surya-mukhi-default-rtdb.asia-southeast1.firebasedatabase.app"})

dummy_data = {
        "-a": {"temperature": 22.5, "timestamp": 1713762000000, "humidity": 60, "min_humidity": 50, "max_humidity": 60},  # 10 AM
        "-b": {"temperature": 23.1, "timestamp": 1713765600000, "humidity": 62, "min_humidity": 52, "max_humidity": 62},  # 11 AM
        "-c": {"temperature": 24.8, "timestamp": 1713769200000, "humidity": 65, "min_humidity": 55, "max_humidity": 65},  # 12 PM
        "-d": {"temperature": 26.3, "timestamp": 1713772800000, "humidity": 58, "min_humidity": 48, "max_humidity": 58},  # 1 PM
        "-e": {"temperature": 28.7, "timestamp": 1713776400000, "humidity": 55, "min_humidity": 45, "max_humidity": 55},  # 2 PM
        "-f": {"temperature": 30.2, "timestamp": 1713780000000, "humidity": 50, "min_humidity": 40, "max_humidity": 50},  # 3 PM
        "-f": {"temperature": 31.5, "timestamp": 1713783600000, "humidity": 48, "min_humidity": 38, "max_humidity": 48},  # 4 PM
        "-g": {"temperature": 32.0, "timestamp": 1713787200000, "humidity": 45, "min_humidity": 35, "max_humidity": 45},  # 5 PM
        "-h": {"temperature": 31.2, "timestamp": 1713790800000, "humidity": 47, "min_humidity": 37, "max_humidity": 47},  # 6 PM
        "-i": {"temperature": 29.8, "timestamp": 1713794400000, "humidity": 52, "min_humidity": 42, "max_humidity": 52},  # 7 PM
        "-j": {"temperature": 27.4, "timestamp": 1713798000000, "humidity": 57, "min_humidity": 47, "max_humidity": 57},  # 8 PM
        "-k": {"temperature": 25.9, "timestamp": 1713801600000, "humidity": 59, "min_humidity": 49, "max_humidity": 59},  # 9 PM
        "-l": {"temperature": 24.5, "timestamp": 1713805200000, "humidity": 61, "min_humidity": 51, "max_humidity": 61},  # 10 PM
        "-m": {"temperature": 23.8, "timestamp": 1713808800000, "humidity": 63, "min_humidity": 53, "max_humidity": 63},  # 11 PM
        "-n": {"temperature": 22.1, "timestamp": 1713812400000, "humidity": 64, "min_humidity": 54, "max_humidity": 64},  # 12 AM
        "-o": {"temperature": 21.7, "timestamp": 1713816000000, "humidity": 66, "min_humidity": 56, "max_humidity": 66},  # 1 AM
        "-p": {"temperature": 20.9, "timestamp": 1713819600000, "humidity": 67, "min_humidity": 57, "max_humidity": 67},  # 2 AM
        "-q": {"temperature": 20.3, "timestamp": 1713823200000, "humidity": 68, "min_humidity": 58, "max_humidity": 68},  # 3 AM
        "-r": {"temperature": 19.8, "timestamp": 1713826800000, "humidity": 69, "min_humidity": 59, "max_humidity": 69},  # 4 AM
        "-s": {"temperature": 19.2, "timestamp": 1713830400000, "humidity": 70, "min_humidity": 60, "max_humidity": 70},  # 5 AM
        "-t": {"temperature": 18.7, "timestamp": 1713834000000, "humidity": 71, "min_humidity": 61, "max_humidity": 71},  # 6 AM
        "-u": {"temperature": 18.3, "timestamp": 1713837600000, "humidity": 72, "min_humidity": 62, "max_humidity": 72},  # 7 AM
        "-v": {"temperature": 17.9, "timestamp": 1713841200000, "humidity": 73, "min_humidity": 63, "max_humidity": 73},  # 8 AM
        "-w": {"temperature": 17.5, "timestamp": 1713844800000, "humidity": 74, "min_humidity": 64, "max_humidity": 74}   # 9 AM
            }

def send_dum():
    try:
        dum_ref=db.reference("WeatherData1")
        dum_ref.set(dummy_data)
        print("dummy sent")
    except Exception as e:
        print(f"Error sending data to Firebase: {e}")

if __name__ == "__main__":
    send_dum()

