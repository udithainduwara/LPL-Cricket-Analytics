import os
import csv
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from dotenv import load_dotenv
from etl.database.models import Match

load_dotenv()

DATABASE_URL =os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("Database URL is missing")

engine = create_engine(DATABASE_URL, future=True)

def load_matches_csv(csv_path: str, engine):
    with Session(engine) as session:                                 #same time open the DB session to write rows 
        with open(csv_path, newline="", encoding="utf-8") as f :     #same time open the csv files 
            reader = csv.DictReader(f)

            for r in reader:
                session.merge(Match(
                    match_id=int(r['match_id']),
                    season_year=int(r["season_year"]) if r.get("season_year") else None,
                    match_number=int(r["match_number"]) if r.get("match_number") else None,
                    match_date=r.get("match_date") or None, 
                    match_type=r.get("match_type") or None,
                    venue=r.get("venue") or None,
                    city=r.get("city") or None,
                    team1_name=r.get("team1_name") or None,
                    team2_name=r.get("team2_name") or None,
                    toss_winner=r.get("toss_winner") or None,
                    toss_decision=r.get("toss_decision") or None,
                    winner=r.get("winner") or None,
                    win_by_runs=int(float(r["win_by_runs"])) if r.get("win_by_runs") else None,
                    win_by_wickets=int(float(r["win_by_wickets"])) if r.get("win_by_wickets") else None,
                    player_of_match=r.get("player_of_match") or None,
                    umpire1=r.get("umpire1") or None,
                    umpire2=r.get("umpir2") or None,
                ))
            session.commit()    
load_matches_csv(r"C:\Users\user\Desktop\CREATING project\CricketAnalytics\data\LPL_2024\Processed\ball_to_ball_data\matches.csv", engine) 

print("Matches table loaded")


'''#Run this as a module on root folder
python -m etl.load.load_sql_mathes
'''