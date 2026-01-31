> **Scope:** This academic project focuses only on LPL 2024 data for analysis. The code and data pipeline will be improved and extended in future iterations.
## Version Control (Git)
- Initialized repository and tracked project structure + datasets
- Commit: `Initialize project with cricket data sources and folder structure`


# WEEK 1 - Collecting and understanding data
- Collected cricket data from multiple sources:
    - Collected ball-by-ball datasets for LPL 2024 by this website (url - https://cricsheet.org/downloads/).
    - Fan comments from social media platforms.

## Fan comments
- Manually collected near 63 fan comments from Facebook, X, and Instagram.
    - Attempted to use X (Twitter) API with Tweepy(Python library), but stopped due to paid API requirements.     
- Used free YouTube Data API googleapiclient(Python library) to fetch 156 fan comments from YouTube.

## Youtube comment fetch (only one video)    
- from dotenv import load_dotenv is used to load environment variables from a .env file so sensitive information like API keys and passwords are kept secure and not hard-coded in the source code.   

- In video address bar after "=" parts is a video id  

- The function(classify_sentiment) analyzes text using keywords and emojis to classify the sentiment.  

- The function(fetch_comments) uses the YouTube Data API to request & collect all comments for a given video, adds sentiment analysis, and returns them as a list of records.

-The function(save_jsonl) saves the records to a JSONL file by writing one JSON object per line.

# Week 2 - create tables

## Firebase Realtime Database(NOSQL)
- Firebase requires json file type, so I merged two files(jsonl type) into one json.
- I create database(LPLCricketAnalytics) and Upload json data into Firebase using python(`json` and `firebase_admin` libraries).
- Provides real-time access to fan comments for analytics.

## PostgreSQL Database(SQL)
- create tables using **SQLAlchemy ORM**:
    - `Match` - match details
    - `MatchPlayer` - players per match and uniqueness constraints
    - `Delivery` - ball-by-ball events(runs, extra, wickets)
- Added indexes and constraints for efficient queries.
- Define relationship between tables for ORM access.
 

       
 