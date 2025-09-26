import os
import requests
import json
import pyttsx3
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv()

USERNAME = os.getenv("USER", "User")
BOTNAME = os.getenv("BOTNAME", "Talksy")

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Default to female voice
engine.setProperty('rate', 190)  # Speed of speech

def speak(text):
    """
    Convert text to speech
    """
    engine.say(text)
    engine.runAndWait()
    return text

def greet_user():
    """
    Greets the user according to the time
    """
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        message = f"Good Morning {USERNAME}"
    elif 12 <= hour < 16:
        message = f"Good Afternoon {USERNAME}"
    elif 16 <= hour < 23:
        message = f"Good Evening {USERNAME}"
    else:
        message = f"It's late, {USERNAME}. You should be sleeping"
    
    return f"{message}. I am {BOTNAME}. How may I assist you?"

def get_weather(city):
    """
    Get current weather data for a city
    """
    api_key = os.getenv("OPENWEATHER_APP_ID")
    if not api_key:
        return "Weather API key is not configured."
        
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code != 200:
            return f"Error getting weather data: {data.get('message', 'Unknown error')}"
        
        weather_desc = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        
        return f"The weather in {city} is {weather_desc}. The temperature is {temperature}°C with humidity at {humidity}% and wind speed of {wind_speed} m/s."
    
    except Exception as e:
        return f"Error getting weather data: {str(e)}"

def get_time():
    """
    Return current time
    """
    now = datetime.datetime.now()
    time_string = now.strftime("%I:%M %p")
    return f"The current time is {time_string}"

def get_date():
    """
    Return current date
    """
    now = datetime.datetime.now()
    date_string = now.strftime("%A, %B %d, %Y")
    return f"Today is {date_string}" 