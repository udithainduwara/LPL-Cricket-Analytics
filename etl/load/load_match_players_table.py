import os
import csv
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError
from etl.database.models import MatchPlayer

load_dotenv()

DATABASE_URL =os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("Database URL is missing")

engine = create_engine(DATABASE_URL, future=True)

def load_match_players_csv(csv_path: str, engine):
    with Session(engine) as session:                                 #same time open the DB session to write rows 
        with open(csv_path, newline="", encoding="utf-8") as f :     #same time open the csv files 
            reader = csv.DictReader(f)

            for r in reader:
                try:                                        #add() can make errors (duplicates insert/FK/NULL rules), so try/except and rollback to handel and continue without crash 
                    session.add(MatchPlayer( 
                        match_id=int(r['match_id']),
                        team_name=(r.get("team_name") or "").strip(),
                        player_name=(r.get("player_name") or "").strip(), 
                    ))
                    session.commit()
                except IntegrityError:
                    session.rollback()
                except Exception as error:
                    session.rollback()
                    print(f"This row {r} has error {error}.")    

            

load_match_players_csv(r"C:\Users\user\Desktop\CREATING project\CricketAnalytics\data\LPL_2024\Processed\ball_to_ball_data\match_players.csv", engine)  

print("load match_players is successful")