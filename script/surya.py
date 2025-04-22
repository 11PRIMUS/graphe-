import firebase_admin
from firebase_admin import credentials, db
import requests
from datetime import datetime
import pandas as pd
import pvlib
import time
import os

from dotenv import load_dotenv
load_dotenv() 

cred = credentials.Certificate(r"C:\pro\suryamukhii\scripts\surya-mukhi-firebase-adminsdk-35jq9-f3122bd9fb.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://surya-mukhi-default-rtdb.asia-southeast1.firebasedatabase.app"
})

OPENWEATHER_API_KEY=os.getenv("OPENWEATHER_API_KEY")

location_ref = db.reference('location')  

while True:
    try:
        location_data = location_ref.get()
        if not location_data or "city" not in location_data:
            print("Location missing")
            time.sleep(25)
            continue
        city=location_data["city"]

        geocode_response = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={OPENWEATHER_API_KEY}"
        )
        geocode_data = geocode_response.json()

        if not geocode_data or len(geocode_data) == 0:
            print(f"Failed to fetch city cord: {city}")
            time.sleep(25)
            continue
        
        lat = location_data["latitude"]
        lon = location_data["longitude"]
        response =requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
        )
        weather =response.json()

        if response.status_code!= 200 or 'weather' not in weather:
            print(f"weather api error Status Code: {response.status_code}")
            print(f"Message: {weather.get('message', 'No error message from API')}")
            time.sleep(25)
            continue

        #weather data
        wind_speed=weather["wind"]["speed"] if "wind" in weather else None
        cloud_cover=weather["clouds"]["all"] if "clouds " in weather else None
        weather_condistion=weather["weather"][0] ["description"]

        now=pd.Timestamp.utcnow()
        solpos=pvlib.solarposition.get_solarposition( #sun position
            time=now,
            latitude=lat,
            longitude=lon
        )

        elevation=float(solpos['elevation'][0])
        azimuth=float(solpos['azimuth'][0])
        
        dni_extra=pvlib.irradiance.get_extra_radiation(now)
        airmass=pvlib.atmosphere.get_relative_airmass(elevation)
        poa_irradiance=pvlib.irradiance.get_total_irradiance(
            surface_tilt=elevation,
            surafce_azimuth=azimuth,
            dni=dni_extra,
            ghi=None,
            dhi=None,
            solar_zenith=90-elevation
        
        )
        irradiance=poa_irradiance["poa_global"]

        print(f"[{now}]Elevation:{elevation:.2f}°,Azimuth:{azimuth:.2f}°,Wind Speed:{wind_speed} m/s, Cloud Cover:{cloud_cover}%, Irradiance:{irradiance:.2f} W/m²")
        ref.set({
                "timestamp":str(now),
                "latitude":lat,
                "longitude":lon,
                "elevation":elevation,
                "azimuth":azimuth,
                "weather":weather_condition,
                "wind_speed":wind_speed,
                "clud_cover":cloud_cover,
                "irradiance":irradiance
            })

    except Exception as e:
        print("[EXCEPTION]", e)

    time.sleep(25)