import json
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
 
load_dotenv()                                           # loads .env from current folder
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY not found. Put API_KEY=YOUR_KEY in your .env file.")
 
VIDEO_ID = "hixu_l5xT6s"                                # In address bar after "=" parts is a video id 
OUTPUT_JSONL = r"C:\Users\user\Desktop\CREATING project\CricketAnalytics\data\LPL_2024\raw\fan_comments_jasonl\lpl_youtube_comments.jsonl" 
FIXED = {
    "tournament": "LPL",
    "season": 2024,
    "platform":"Youtube",
    "language": "en",
    "collected_at": "2026-01-24"
}

 
def classify_sentiment(text):
    t = text.lower()

    if any(e in text for e in ["🔥", "🤯", "💥", "😍", "🥵"]):
        return "excitement"
    if any(e in text for e in ["🏆", "🎉", "🥳", "❤️", "💙"]):
        return "joy"
    if any(e in text for e in ["💔", "😢", "😭"]):
        return "disappointment"

    anger_words = ["hate", "stupid", "idiot", "trash", "worst", "pathetic", "angry", "shame on", "disgusting"]
    sarcasm_markers = ["yeah right", "sure", "lol", "lmao", "as if", "nice one", "/s"]
    disappointment_words = ["sad", "unlucky", "heartbroken", "pain","disappointed", "missed", "lost","couldn't", "can't believe"]
    frustration_words = ["why", "should have", "could have", "waste", "bad decision", "not fair", "rigged"]
    pride_words = ["proud", "on the top","number 1", "no.1", "king", "great achievement", "record"]
    joy_words = ["congrats", "congratulations", "happy", "love", "champion","trophy", "yay"]
    excitement_words = ["wow", "unreal", "insane", "fire",  "lit", "goat", "legend", "best", "amazing", "brilliant"]

    if any(w in t for w in anger_words):
        return "anger"
    if any(w in t for w in sarcasm_markers):
        return"sarcasm"
    if any(w in t for w in disappointment_words):
        return "disappointment"
    if any(w in t for w in frustration_words):
        return "frustration"
    if any(w in t for w in pride_words):
        return "pride"
    if any(w in t for w in joy_words):
        return "joy"
    if any(w in t for w in excitement_words):
        return "excitement"

    return"neutral"

 
def fetch_comments(video_id, api_key):
    youtube = build("youtube", "v3", developerKey=api_key)   

    records = []
    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token,
            textFormat = "plainText",
            order = "time"
        )
        response = request.execute()

        for item in response.get("items", []):              # Using dict.get(key, default) with fallback values to avoid KeyError and crash code, if a field is missing.
            top = item["snippet"]["topLevelComment"]
            snip = top["snippet"]

            comment_id =top["id"]
            comment_text =snip.get("textDisplay", "")
            author_name =snip.get("authorDisplayName", "")
            created_at =snip.get("publishedAt", "")
            post_url =f"https://www.youtube.com/watch?v={video_id}&lc={comment_id}"

            record = {
                **FIXED,
                "comment_text": comment_text,
                "author_name": author_name,
                "sentiment" : classify_sentiment(comment_text),
                "created_at": created_at,
                "post_url": post_url
            }
            records.append(record)

        next_page_token = response.get("nextPageToken")
        if next_page_token is None:                         # Stop looping when there is no next page token (no more pages).                     
            break                                           # this will not stop for "", [], 0

    return records

 
def save_jsonl(path, records):
    with open(path,"w",encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

 
if __name__ == "__main__": 
    data = fetch_comments(VIDEO_ID, API_KEY)         #This means the comments will be fetched only when I run the file directly, not when I import it.       

    save_jsonl(OUTPUT_JSONL, data)
    

    print("Done")
    print("Total comments: ", len(data))
 
  
 
