import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import requests
import os
import time
import schedule
import pandas as pd
import pvlib

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
        print("Fetched location data:", location_data)
        
        if location_data and "lat" in location_data and "long" in location_data:
            return location_data["latitude"], location_data["longitude"]

        raise ValueError("Latitude or Longitude not found in Firebase")
    except Exception as e:
        print(f"Error fetching location from Firebase: {e}")
        return None, None

def fetch_weather_data(lat, lon):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

    try:
        response = requests.get(weather_url)
        weather = response.json()
        if response.status_code != 200 or "weather" not in weather:
            print(f"Weather API error. Status Code: {response.status_code}")
            print(f"Message: {weather.get('message', 'No error message from API')}")
            return None

        temperature = weather["main"]["temp"]
        wind_speed = weather["wind"]["speed"] if "wind" in weather else None
        cloud_cover = weather["clouds"]["all"] if "clouds" in weather else None
        weather_condition = weather["weather"][0]["description"]

        #solar pos
        now = pd.Timestamp.utcnow()
        solpos = pvlib.solarposition.get_solarposition(
            time=now,
            latitude=lat,
            longitude=lon
        )
        elevation = float(solpos["elevation"][0])
        azimuth = float(solpos["azimuth"][0])

        #solar irradiance
        dni_extra = pvlib.irradiance.get_extra_radiation(now)
        airmass = pvlib.atmosphere.get_relative_airmass(elevation)
        poa_irradiance = pvlib.irradiance.get_total_irradiance(
            surface_tilt=elevation,
            surface_azimuth=azimuth,
            dni=dni_extra,
            ghi=None,
            dhi=None,
            solar_zenith=90 - elevation
        )
        irradiance = poa_irradiance["poa_global"]

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {
            "temperature": temperature,
            "timestamp": timestamp,
            "elevation": elevation,
            "azimuth": azimuth,
            "weather": weather_condition,
            "wind_speed": wind_speed,
            "cloud_cover": cloud_cover,
            "irradiance": irradiance
        }
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def send_weather_data_to_firebase(weather_data):
    try:
        weather_ref = db.reference("WeatherData2")
        weather_ref.set(weather_data)
    except Exception as e:
        print(f"Error sending data to Firebase: {e}")

def job():
    lat, lon = fetch_location_from_firebase()
    if lat is not None and lon is not None:
        weather_data = fetch_weather_data(lat, lon)
        if weather_data:
            send_weather_data_to_firebase(weather_data)

if __name__ == "__main__":
    schedule.every(5).minutes.do(job)

    print("Data collection started")
    while True:
        schedule.run_pending()
        time.sleep(5)