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

def fetch_requnit():
    try:
        requnit_ref=db.firebase("required_unit")
        requnit_data=requnit_ref.get()
        print(f"fetched unit :{requnit_data}")
