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

API_KEY=os.getenv("OPENWEATHER_API_KEY")
location_ref=db.reference("location")
ref =db.reference("/sun_position")



while True:
    try:
        location_data=location_ref.get()
        if not location_data or "lat" not in location_data or "long" not in location_data:
            print("location is missing")
            time.sleep(5)
            continue

        lat=location_data["lat"]
        long=location_data["long"]


        response =requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={API_KEY}"
        )
        weather =response.json()

        if response.status_code!= 200 or 'weather' not in weather:
            print(f"weather api error Status Code: {response.status_code}")
            print(f"Message: {weather.get('message', 'No error message from API')}")
        else:
            now=pd.Timestamp.utcnow()
            solpos=pvlib.solarposition.get_solarposition( #sun position
                time=now,
                latitude=lat,
                longitude=long
            )

            elevation=float(solpos['elevation'][0])
            azimuth=float(solpos['azimuth'][0])

            print(f"[{now}]Elevation:{elevation:.2f}°,Azimuth:{azimuth:.2f}°")

            ref.set({
                "timestamp":str(now),
                "elevation":elevation,
                "azimuth":azimuth,
                "weather":weather["weather"][0]["description"]
            })

    except Exception as e:
        print("[EXCEPTION]", e)

    time.sleep(5)