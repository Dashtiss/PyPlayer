import MusicBot
import os
from dotenv import load_dotenv
from MusicBot.error import error, warn
import requests





# Put your token here or in a .env file
TOKEN = ""

if not TOKEN:
    warn("TOKEN variable not filled, Getting from .env file")
    if os.path.exists(".env"):
        load_dotenv()
        try:
            TOKEN = os.environ["TOKEN"]
        except KeyError:
            error("TOKEN was not found in .env file. Please check that you have put it in and spelled it correctly")
            exit(1)
    else:
        error(".env file doesn't exist. Please read the README file for information on how to set it up")
        exit(1)
"""
url = "https://accounts.spotify.com/api/token"
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
payload = {
    "grant_type": "client_credentials",
    "client_id": os.environ["ClientID"],
    "client_secret": os.environ["ClientSecret"]
}

response = requests.post(url, headers=headers, data=payload)

# Printing the response to see the result
print(response.json())"""
print("Starting Bot")

MusicBot.Startup(TOKEN)
