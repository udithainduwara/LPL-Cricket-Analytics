import os, glob, json
import pandas as pd

IN_DIR  = r"C:\Users\user\Desktop\CREATING project\CricketAnalytics\data\Ball to Ball Data LPL2024"
OUT_DIR = r"C:\Users\user\Desktop\CREATING project\CricketAnalytics\data\LPL2024_csv_out"
os.makedirs(OUT_DIR, exist_ok=True)

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

def make_match_id(season_year, match_number, used):
    # Create readable id like 2024001, 2024002 ...
    if season_year is not None and match_number is not None:
        mid = season_year * 1000 + match_number
    else:
        mid = 1

    while mid in used:   # avoid duplicates
        mid += 1
    used.add(mid)
    return mid

matches, players, deliveries = [], [], []
used_ids = set()

for path in sorted(glob.glob(os.path.join(IN_DIR, "*.json"))):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    info = data.get("info") or {}
    event = info.get("event") or {}
    teams = info.get("teams") or []


    season_year  = int_or_none(info.get("season_year", info.get("season")))
    match_number = int_or_none(event.get("match_number"))
    match_id = make_match_id(season_year, match_number, used_ids)

    # ---- MATCH ROW (matches table columns) ----
    officials = info.get("officials", {}) or {}
    umpires = (officials.get("umpires") or info.get("umpires") or [])


    outcome = info.get("outcome", {}) or {}
    by = outcome.get("by", {}) or {}

    matches.append({
        "match_id": match_id,
        "season_year": season_year,
        "match_number": match_number,
        "match_date": (info.get("dates") or [None])[0],
        "match_type": info.get("match_type"),
        "venue": info.get("venue"),
        "city": info.get("city"),
        "team1_name": teams[0] if len(teams) > 0 else None,
        "team2_name": teams[1] if len(teams) > 1 else None,
        "toss_winner": (info.get("toss", {}) or {}).get("winner"),
        "toss_decision": (info.get("toss", {}) or {}).get("decision"),
        "winner": outcome.get("winner"),
        "win_by_runs": int_or_none(by.get("runs")),
        "win_by_wickets": int_or_none(by.get("wickets")),
        "player_of_match": (info.get("player_of_match") or [None])[0],
        "umpire1": umpires[0] if len(umpires) > 0 else None,
        "umpire2": umpires[1] if len(umpires) > 1 else None,
    })

    # ---- PLAYERS ROWS (match_players table columns) ----
    for team_name, plist in (info.get("players", {}) or {}).items():
        for player_name in (plist or []): 
            players.append({
                "match_id": match_id,
                "team_name": team_name,
                "player_name": player_name
            })

    # ---- DELIVERY ROWS (deliveries table columns) ----
    for innings_no, inning in enumerate(data.get("innings", []), start=1):
        batting_team = inning.get("team")

        for over_obj in inning.get("overs", []):
            over_no = int_or_0(over_obj.get("over"))
            ball_no = 0

            for d in over_obj.get("deliveries", []):
                ball_no += 1

                runs = d.get("runs", {}) or {}
                extras = d.get("extras", {}) or {}
                wickets = d.get("wickets", []) or []

                deliveries.append({
                    "match_id": match_id,
                    "innings_no": innings_no,
                    "batting_team": batting_team,
                    "over_no": over_no,
                    "ball_no": ball_no,
                    "batter": d.get("batter"),
                    "bowler": d.get("bowler"),
                    "non_striker": d.get("non_striker"),
                    "runs_batter": int_or_0(runs.get("batter")),
                    "runs_extras": int_or_0(runs.get("extras")),
                    "runs_total": int_or_0(runs.get("total")),
                    "wide": int_or_0(extras.get("wides")),
                    "noball": int_or_0(extras.get("noballs")),
                    "bye": int_or_0(extras.get("byes")),
                    "legbye": int_or_0(extras.get("legbyes")),
                    "wicket": 1 if wickets else 0,
                    "player_out": wickets[0].get("player_out") if wickets else None,
                    "dismissal_kind": wickets[0].get("kind") if wickets else None,
                })

# Save CSVs (drop_duplicates avoids breaking your UNIQUE constraint)
pd.DataFrame(matches).to_csv(os.path.join(OUT_DIR, "matches.csv"), index=False)
pd.DataFrame(players).drop_duplicates().to_csv(os.path.join(OUT_DIR, "match_players.csv"), index=False)
pd.DataFrame(deliveries).to_csv(os.path.join(OUT_DIR, "deliveries.csv"), index=False)

print("DONE ✅ CSV files created in:", OUT_DIR)
