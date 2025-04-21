import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import requests
import os
import time



cred = credentials.Certificate(r"C:\pro\suryamukhii\scripts\surya-mukhi-firebase-adminsdk-35jq9-f3122bd9fb.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://surya-mukhi-default-rtdb.asia-southeast1.firebasedatabase.app"
})

def fetch_power():
    try:
        power_ref=db.reference("SensorData/Power")
        power_value=power_ref.get()
        print(f"fetched power value:{power_value}")

        if power_value is not None and isinstance(power_value,(int,float)):
            status =0 if power_value<70 else 1
            print(f"power is {'below'if status ==0 else 'above'} 70. Setting status to {status}.")

            status_ref=db.reference("status")
            status_ref.set(status)
            print(f"updated to {status} ")
        
        else:
            print("invalid power value")
    except Exception as e:
        print(f"error fetching and updating power data:{e}")
if __name__=="__main__":
    fetch_power()