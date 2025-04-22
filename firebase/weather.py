import firebase_admin
from firebase_admin import credentials, db
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r"C:\pro\suryamukhii\scripts\surya-mukhi-firebase-adminsdk-35jq9-f3122bd9fb.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://surya-mukhi-default-rtdb.asia-southeast1.firebasedatabase.app"
})

def fetch_weather_data(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        #temp_min = data["main"].get("temp_min")
        #temp_max = data["main"].get("temp_max")

        return {
            "temperature": temperature,
            "humidity": humidity,
           # "temp_min": temp_min,
            #"temp_max": temp_max
            
        }
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

def send_weather_data_to_firebase(weather_data2):
    try:
        weather_ref = db.reference("WeatherData2")
        # Update the data in WeatherData2
        weather_ref.update(weather_data2)
        print("Updated temperature and humidity in Firebase:", weather_data2)
    except Exception as e:
        print(f"Error updating data in Firebase: {e}")

def location_listener(event):
    try:
        # Get the updated location from the event
        location_data = event.data
        print("Location changed:", location_data)

        # Check if the location data is valid
        if isinstance(location_data, dict) and "location" in location_data:
            city = location_data["location"]
            weather_data2 = fetch_weather_data(city)
            if weather_data2:
                send_weather_data_to_firebase(weather_data2)
        else:
            print("Invalid location data")
    except Exception as e:
        print(f"Error in location listener: {e}")

if __name__ == "__main__":
    print("Listening for location changes...")
    # Add a listener to the "location" node in Firebase
    location_ref = db.reference("location")
    location_ref.listen(location_listener)