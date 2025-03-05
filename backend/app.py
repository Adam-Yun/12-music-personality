import requests, os, json
from datetime import datetime, timedelta
from dotenv import load_dotenv, set_key
from app_time import *

# Load variables from .env file
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Get the Spotify access token data
def setCredentials(client_id, client_secret):
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, headers=headers, data=data)

    os.environ["SPOTIFY_ACCESS_TOKEN"] = response.json()['access_token']
    os.environ["SPOTIFY_TOKEN_TYPE"] = response.json()['token_type']
    os.environ["SPOTIFY_EXPIRES_IN"] = str(response.json()['expires_in'])
    timestamp = datetime.now()
    expiry = timestamp + timedelta(seconds=int(os.getenv("SPOTIFY_EXPIRES_IN")))
    os.environ["SPOTIFY_ACCESS_TOKEN_ISSUED_TIME"] = timeToString(timestamp)
    os.environ["SPOTIFY_ACCESS_TOKEN_EXPIRY_TIME"] = timeToString(expiry)

    envPath = ".env"
    set_key(envPath, "SPOTIFY_ACCESS_TOKEN", os.environ['SPOTIFY_ACCESS_TOKEN'])
    set_key(envPath, "SPOTIFY_TOKEN_TYPE", os.environ['SPOTIFY_TOKEN_TYPE'])
    set_key(envPath, "SPOTIFY_EXPIRES_IN", os.environ['SPOTIFY_EXPIRES_IN'])
    set_key(envPath, "SPOTIFY_ACCESS_TOKEN_ISSUED_TIME", os.environ['SPOTIFY_ACCESS_TOKEN_ISSUED_TIME'])
    set_key(envPath, "SPOTIFY_ACCESS_TOKEN_EXPIRY_TIME", os.environ['SPOTIFY_ACCESS_TOKEN_EXPIRY_TIME'])

# Checks if the access token is expired, return True if expired False if not
def checkExpiry():
    time = datetime.now()
    # print(f'Current Time : {time}')
    timestamp = stringToTime(os.getenv("SPOTIFY_ACCESS_TOKEN_ISSUED_TIME"))
    expiry = stringToTime(os.getenv("SPOTIFY_ACCESS_TOKEN_EXPIRY_TIME"))

    # If timestamp has a false value in primitive data type
    if not timestamp:
        return True
    # Check if timestamp is expired
    else:
        if time > expiry:
            return True
        elif time < expiry:
            return False
        else:
            return "!Timestamp Error"

def printCredentials():
    print(f'SPOTIFY_ACCESS_TOKEN : {os.getenv("SPOTIFY_ACCESS_TOKEN")}')
    print(f'SPOTIFY_TOKEN_TYPE : {os.getenv("SPOTIFY_TOKEN_TYPE")}')
    print(f'SPOTIFY_EXPIRES_IN : {os.getenv("SPOTIFY_EXPIRES_IN")}')
    print(f'SPOTIFY_ACCESS_TOKEN_ISSUED_TIME : {os.getenv("SPOTIFY_ACCESS_TOKEN_ISSUED_TIME")}')
    print(f'SPOTIFY_ACCESS_TOKEN_EXPIRY_TIME : {os.getenv("SPOTIFY_ACCESS_TOKEN_EXPIRY_TIME")}')

if checkExpiry():
    print("Expire? True")
    setCredentials(CLIENT_ID,CLIENT_SECRET)
    # printCredentials()
else:
    print("Expire? False")
    # printCredentials()