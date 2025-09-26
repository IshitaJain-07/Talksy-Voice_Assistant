import os
from dotenv import load_dotenv
from datetime import datetime
import random

# Load environment variables
load_dotenv()

# Set environment variables directly (fallback to .env values if present)
# Change these to your actual values
USERNAME = os.getenv("USER", "Janvi")
BOTNAME = os.getenv("BOTNAME", "Talksy")

# Opening responses
opening_text = [
    "I'm ready to assist you.",
    "What can I help you with?",
    "How may I assist you today?",
    "I'm listening.",
    "Ready for your command.",
    "At your service.",
    "What would you like me to do?",
    "I'm here to help."
]

# Get time of day
def get_time():
    """Return current time"""
    now = datetime.now()
    time_string = now.strftime("%I:%M %p")
    return f"The current time is {time_string}"

# Get current date
def get_date():
    """Return current date"""
    now = datetime.now()
    date_string = now.strftime("%A, %B %d, %Y")
    return f"Today is {date_string}"

# Random choice from list
def random_choice(items):
    """Select a random item from a list"""
    return random.choice(items) 