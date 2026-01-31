import json

json_list = []

jsonl_files = [r"C:\Users\user\Desktop\CREATING project\CricketAnalytics\data\fb_X_fans_comments.jsonl", r"C:\Users\user\Desktop\CREATING project\CricketAnalytics\data\lpl_youtube_comments.jsonl"]

for file in jsonl_files:
    with open(file, "r") as f:
        for line in f:
            json_list.append(json.loads(line))

with open(r"C:\Users\user\Desktop\CREATING project\CricketAnalytics\data\fan_comments LPL2024\LPL_fan_comments.json", "w") as f:
    json.dump(json_list, f, indent=2)

print("Conversion is succesfull")




