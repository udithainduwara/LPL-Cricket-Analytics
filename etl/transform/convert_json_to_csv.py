import os, glob, json
import pandas

input_directory = r"C:\Users\user\Desktop\CREATING project\CricketAnalytics\data\LPL_2024\raw\ball_to_ball_data"
Output_directory = r"C:\Users\user\Desktop\CREATING project\CricketAnalytics\data\LPL_2024\Processed\ball_to_ball_data"

def int_or_none(x):
    try:
        return int(x)
    except:
        return None
    
def int_or_0(x):
    try:
        return int(x)
    except:
        return 0

matches, match_players, deliveries = [], [], []

for path in sorted(glob.glob(os.path.join(input_directory, "*.json"))):
    with open(path, "r", encoding="utf-8") as f:
        data=json.load(f)

    info = data.get("info") or {}
    event = info.get("event") or {}
    teams = info.get("teams") or []
     

    match_id = int_or_none(info.get("match_id"))
    if match_id is None:                             # match_id is required (used as primary key / foreign key). Stop if missing. 
        raise ValueError(f"match_id is missing in this {path}")


    season_year = int_or_none(info.get("season"))
    match_number = int_or_0(event.get("match_number"))
 
    officials = info.get("officials", {}) or {}
    umpires = (officials.get("umpires") or info.get("umpires") or [])
    outcome = info.get("outcome", {}) or {}
    win_by = outcome.get("by", {}) or {}
    
    '''
    for matches table
    '''
    matches.append({                                               
        "match_id": match_id,
        "season_year": season_year,  
        "match_number": match_number,  
        "match_date": (info.get("dates") or [None])[0],  
        "match_type":  info.get("match_type"),
        "venue": info.get("venue"),  
        "city": info.get("city"),  
        
        "team1_name": teams[0] if len (teams) > 0 else None, 
        "team2_name": teams[1] if len (teams) > 1 else None,
        
        "toss_winner": (info.get("toss", {})or {}).get("winner"),
        "toss_decision": (info.get("toss", {})or {}).get("decision"), 
        
        "winner": outcome.get("winner"),
        "win_by_runs": int_or_none(win_by.get("runs")),
        "win_by_wickets": int_or_none(win_by.get("wickets")),
        "player_of_match": (info.get("player_of_match") or [None])[0],

        "umpire1": umpires[0] if len(umpires) > 0 else None,
        "umpire2": umpires[1] if len(umpires) > 1 else None,
    })

    for team_name, players_list in (info.get("players", {}) or {}).items():
        for player_name in (players_list or []): 
            match_players.append({
                "match_id": match_id,
                "team_name": team_name,
                "player_name": player_name
            })
 
    for innings_no, inning in enumerate(data.get("innings", []), start=1):
        batting_team = inning.get("team")

        for over_data in inning.get("overs", []):
            over_no = int_or_0(over_data.get("over"))
            ball_no = 0

            for delivery_data in over_data.get("deliveries", []):
                ball_no +=1
            
                runs = delivery_data.get("runs", {}) or {}
                extras = delivery_data.get("extras", {}) or {}
                wickets = delivery_data.get("wickets", []) or []

                deliveries.append({
                    "match_id": match_id,  
 
                    "innings_no": innings_no,
                    "batting_team": batting_team,
                    
                    "over_no": over_no,
                    "ball_no": ball_no,
                    
                    "batter": delivery_data.get("batter"),
                    "bowler": delivery_data.get("bowler"),
                    "non_striker": delivery_data.get("non_striker"), 
                    
                    "runs_batter": int_or_0(runs.get("batter")),
                    "runs_extras": int_or_0(runs.get("extras")), 
                    "runs_total": int_or_0(runs.get("total")), 
                    
                    "wide": int_or_0(extras.get("wides")),
                    "noball": int_or_0(extras.get("noballs")),
                    "bye": int_or_0(extras.get("byes")), 
                    "legbye": int_or_0(extras.get("legbyes")), 
                    
                    "wicket": 1 if len(wickets) > 0 else 0,
                    "player_out": wickets[0].get("player_out") if wickets else None,
                    
                    "wicket_type": wickets[0].get("kind") if wickets else None,
                
                })

pandas.DataFrame(matches).to_csv(os.path.join(Output_directory, "matches.csv"), index=False)
pandas.DataFrame(match_players).drop_duplicates().to_csv(os.path.join(Output_directory, "match_players.csv"), index=False)
pandas.DataFrame(deliveries).to_csv(os.path.join(Output_directory, "deliveries.csv"), index=False)   

print("Conversion successful")
