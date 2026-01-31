import json
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate(r"C:\Users\user\Desktop\CREATING project\CricketAnalytics\config\serviceAccountKey.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://lplcricketanalytics-default-rtdb.firebaseio.com/"})


with open(r"C:\Users\user\Desktop\CREATING project\CricketAnalytics\data\fan_comments LPL2024\LPL_fan_comments.json", "r") as f:
    LPL_fan_comments = json.load(f)

ref = db.reference("/LPL_fan_comments")
ref.set(LPL_fan_comments)

print("Ok")
