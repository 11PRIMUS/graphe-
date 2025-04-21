import firebase_admin
from firebase_admin import credentials, db
import joblib
import numpy as np
from datetime import datetime

cred = credentials.Certificate("scripts/surya-mukhi-firebase-adminsdk-35jq9-f3122bd9fb.json")  
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://surya-mukhi-default-rtdb.asia-southeast1.firebasedatabase.app"
})

#models
model = joblib.load("scripts/trained_model.pkl")
scaler = joblib.load("scripts/scaler.pkl")

weather_map = {
    "clear sky": [1, 0, 0],
    "cloudy sky": [0, 1, 0],
    "partly cloudy": [0, 0, 1],
}

def fetch_realtime_data():
    weather_data_ref = db.reference("WeatherData")
    solar_data_ref = db.reference("solar_data")
    
    weather_data = weather_data_ref.get()
    solar_data = solar_data_ref.get()

    if not weather_data or not solar_data:
        raise ValueError("Data missing from Firebase.")
    
    if isinstance(weather_data, list):
        print("Weather data is a list. Extracting the first element.")
        weather_data = weather_data[0]
    if isinstance(solar_data, list):
        print("Solar data is a list. Extracting the first element.")
        solar_data = solar_data[0]

    combined_data = {**weather_data, **solar_data}
    print("Fetched data:", combined_data)  
    return combined_data

def transform_data(data):
    try:
        #check dict data
        if isinstance(data, list):
            print("Data is a list. Extracting the first element.")  
            data = data[0] 

        timestamp = data["timestamp"]
        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

        #feature extraction
        hour = dt.hour
        day_of_year = dt.timetuple().tm_yday
        month = dt.month

        weather_condition = data["weather_condition"]
        if weather_condition not in weather_map:
            raise ValueError(f"Unknown weather condition: {weather_condition}")

        weather_encoded = weather_map[weather_condition]
        irradiance = data.get("irradiance", 1000) 

        #features
        features = [
            hour,
            day_of_year,
            month,
            data["elevation"],  
            data["azimuth"],    
            data["temperature"],
            data["humidity"],
            data["pressure"],
            data["wind_speed"],
        ] + weather_encoded + [irradiance]  

        return np.array(features).reshape(1, -1)
    except KeyError as e:
        raise KeyError(f"Missing key in data: {e}")
    except Exception as e:
        raise Exception(f"Error transforming data: {e}")


def predict_output(features):
    try:
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)
        tilt_x, tilt_y = prediction[0]  
        print(f"Predicted tilt_x: {tilt_x}, tilt_y: {tilt_y}")
        return tilt_x, tilt_y
    except Exception as e:
        print(f"Error during prediction: {e}")
def send_prediction_to_firebase(tilt_x, tilt_y):
    try:
        tilt_data_ref = db.reference("PredictedTiltData")

        tilt_data = {
            "tilt_x": tilt_x,
            "tilt_y": tilt_y,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        #write to firebase
        tilt_data_ref.push(tilt_data)
        print("Predicted tilt data sent to Firebase successfully.")
    except Exception as e:
        print(f"Error sending data to Firebase: {e}")

if __name__ == "__main__":
    try:
        raw_data = fetch_realtime_data()
        formatted_data = transform_data(raw_data)
        tilt_x, tilt_y = predict_output(formatted_data)
        send_prediction_to_firebase(tilt_x, tilt_y)

    except Exception as e:
        print(f"Error: {e}")