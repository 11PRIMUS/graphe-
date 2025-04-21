import firebase_admin
from firebase_admin import crededntials,db

def initialize_firebase():
    cred=crededntials.Certificate("")
    firebase_admin.initialize_app(cred,{'databaseURL': 'https://surya-mukhi-default-rtdb.asia-southeast1.firebasedatabase.app/'})
    print("firebase initialized")
initialize_firebase()