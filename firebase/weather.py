import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import requests
import os
import time
import schedule

from dotenv import load_dotenv
load_dotenv() 

cred = credentials.Certificate(r"C:\pro\suryamukhii\scripts\surya-mukhi-firebase-adminsdk-35jq9-f3122bd9fb.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://surya-mukhi-default-rtdb.asia-southeast1.firebasedatabase.app"
})

def fetch_location_from_firebase():
    try:
        location_ref = db.reference("location")
        location_data = location_ref.get()
        print("fetched location data:", location_data)
        if isinstance(location_data, str):
            return location_data
        raise ValueError("City not found")
    except Exception as e:
        print(f"Error fetching location from Firebase: {e}")
        return None  

def fetch_weather_data(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")  
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        temperature = data["main"]["temp"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date = datetime.now().strftime("%Y-%m-%d")
        day = datetime.now().strftime("%A")
        return {
            "temperature": temperature,
            "timestamp": timestamp,
            "date": date,
            "day": day
        }
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def send_weather_data_to_firebase(weather_data1):
    try:
        weather_ref = db.reference("WeatherData1")
        weather_ref.push(weather_data1)
        print("sent to firebase")
    except Exception as e:
        print(f"Error sending : {e}")

def job():
    city = fetch_location_from_firebase()
    if city:
        weather_data1 = fetch_weather_data(city)
        if weather_data1:
            send_weather_data_to_firebase(weather_data1)

if __name__ == "__main__":
    schedule.every(1).minutes.do(job)

    print("data collection started")
    while True:
        schedule.run_pending()
        time.sleep(1)  