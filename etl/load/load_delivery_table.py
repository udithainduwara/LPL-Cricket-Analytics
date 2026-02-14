import os, csv
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from etl.database.models import Delivery

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("Database URL is missing")

engine = create_engine(DATABASE_URL, future=True)

def to_int(v, default=0):
    v = (v or "").strip()
    if v == "" :
        return default
    return int(float(v))  #csv file float(10.0) convert to int(10) because my models

def load_deliveries_csv(csv_path: str, engine):
    with Session(engine) as session,open(csv_path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:                                       #add() can make errors (duplicates insert/FK/NULL rules), so try/except and rollback to handel and continue without crash 
                session.add(Delivery(
                    match_id = int(r["match_id"]), 
                    innings_no=to_int(r.get("innings_no"), 0),
                    batting_team=r.get("batting_team") or None,
                    over_no=to_int(r.get("over_no"), 0),
                    ball_no=to_int(r.get("ball_no"), 0),
                    batter=r.get("batter") or None,
                    bowler=r.get("bowler") or None,
                    non_striker=r.get("non_striker") or None,
                    runs_batter=to_int(r.get("runs_batter"), 0),
                    runs_extras=to_int(r.get("runs_extras"), 0),
                    runs_total=to_int(r.get("runs_total"), 0),
                    wide=to_int(r.get("wide"), 0),
                    noball=to_int(r.get("noball"), 0),
                    bye=to_int(r.get("bye"), 0),
                    legbye=to_int(r.get("legbye"), 0),
                    wicket=to_int(r.get("wicket"), 0),
                    player_out=r.get("player_out") or None,
                    wicket_type=r.get("wicket_type") or None,
                ))
                session.commit()

            except IntegrityError:
                session.rollback()  #duplicate row /NOT NULL skip and continue
            except Exception as error:
                session.rollback()
                print(f"This row {r} has error {error}.")    

load_deliveries_csv(r"C:\Users\user\Desktop\CREATING project\CricketAnalytics\data\LPL_2024\Processed\ball_to_ball_data\deliveries.csv", engine)

print("deliveries table loaded successfully")
