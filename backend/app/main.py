from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pyttsx3
import speech_recognition as sr
import os
import uvicorn
from datetime import datetime
from random import choice

# Import functionality
from .utils import opening_text, USERNAME, BOTNAME, get_time, get_date
from .functions.online_ops import (
    find_my_ip, get_latest_news, get_random_advice, get_random_joke,
    get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia,
    send_email, send_whatsapp_message
)
from .functions.os_ops import (
    open_calculator, open_camera, open_cmd, open_notepad, open_discord
)

app = FastAPI(title="Talksy API", description="API for the Talksy virtual assistant")

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Default to female voice
engine.setProperty('rate', 190)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume

# Initialize Speech Recognition
recognizer = sr.Recognizer()
recognizer.pause_threshold = 1  # Seconds of silence before the phrase is considered complete
recognizer.energy_threshold = 300  # Minimum audio energy to consider for recording

# Model classes
class TextCommand(BaseModel):
    command: str

class ListenRequest(BaseModel):
    timeout: int = 5

class SpeakRequest(BaseModel):
    text: str

class EmailRequest(BaseModel):
    receiver_address: str
    subject: str
    message: str

class WhatsAppRequest(BaseModel):
    number: str
    message: str

class WikipediaRequest(BaseModel):
    query: str

class YoutubeRequest(BaseModel):
    query: str

class GoogleRequest(BaseModel):
    query: str

class WeatherRequest(BaseModel):
    city: str

# Text to Speech
def speak(text):
    """Convert text to speech"""
    try:
        engine.say(text)
        engine.runAndWait()
        return text
    except Exception as e:
        print(f"TTS Error: {str(e)}")
        return text

# Listen for voice
def listen_for_command(timeout=5):
    """Listen for a voice command"""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
            print("Processing...")
            
            command = recognizer.recognize_google(audio, language='en-US')
            command = command.lower()
            print(f"User said: {command}")
            return command
    except sr.WaitTimeoutError:
        return "Timeout occurred while waiting for speech"
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand what you said."
    except sr.RequestError as e:
        return f"Could not request results; {e}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Greet user
def greet_user():
    """Greet the user according to the time"""
    hour = datetime.now().hour
    if 6 <= hour < 12:
        greeting = f"Good Morning {USERNAME}"
    elif 12 <= hour < 16:
        greeting = f"Good Afternoon {USERNAME}"
    elif 16 <= hour < 23:
        greeting = f"Good Evening {USERNAME}"
    else:
        greeting = f"It's late, {USERNAME}. You should be sleeping"
    
    return f"{greeting}. I am {BOTNAME}. How may I assist you?"

# Process command
def process_command(query):
    """Process user command and execute appropriate action"""
    if not query or query.isspace():
        return "I didn't receive a command."
    
    query = query.lower().strip()
    response = ""
    
    # Check for exit commands
    if 'exit' in query or 'stop' in query or 'bye' in query or 'goodbye' in query:
        hour = datetime.now().hour
        if hour >= 21 or hour < 6:
            response = "Good night! Take care!"
        else:
            response = "Have a good day!"
        return response
    
    # Process commands - first check for exact matches, then partial ones
    
    # Joke commands - prioritized for better joke recognition
    if any(word in query for word in ['joke', 'funny', 'laugh', 'humor', 'comedy']):
        response = get_random_joke()
    
    elif 'advice' in query:
        response = get_random_advice()
    
    elif 'ip address' in query:
        ip_address = find_my_ip()
        response = f'Your IP Address is {ip_address}'
    
    elif 'wikipedia' in query and 'search' in query:
        # This will be processed in a separate endpoint
        response = "Please use the specific Wikipedia search endpoint."
    
    elif 'youtube' in query and 'play' in query:
        # This will be processed in a separate endpoint
        response = "Please use the specific YouTube play endpoint."
    
    elif 'search' in query and 'google' in query:
        # This will be processed in a separate endpoint
        response = "Please use the specific Google search endpoint."
    
    elif 'whatsapp message' in query:
        # This will be processed in a separate endpoint
        response = "Please use the specific WhatsApp message endpoint."
    
    elif 'email' in query:
        # This will be processed in a separate endpoint
        response = "Please use the specific email endpoint."
    
    elif 'news' in query:
        news = get_latest_news()
        response = "\n".join(news)
    
    elif 'weather' in query:
        # This will be processed in a separate endpoint
        response = "Please use the specific weather endpoint."
    
    elif 'time' in query:
        response = get_time()
    
    elif 'date' in query:
        response = get_date()
    
    elif 'open notepad' in query:
        response = open_notepad()
    
    elif 'open discord' in query:
        response = open_discord()
    
    elif 'open command prompt' in query or 'open cmd' in query:
        response = open_cmd()
    
    elif 'open camera' in query:
        response = open_camera()
    
    elif 'open calculator' in query:
        response = open_calculator()
    
    else:
        # If no specific command matches
        response = "I'm not sure how to help with that. Can you be more specific?"
    
    return response

# API Endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to Talksy API. A virtual assistant that respects your privacy."}

@app.get("/greet")
async def greet():
    """Get a greeting based on the time of day"""
    greeting = greet_user()
    return {"message": greeting, "spoken": speak(greeting)}

@app.post("/process-text")
async def process_text_command(command: TextCommand):
    """Process a text command"""
    try:
        result = process_command(command.command)
        return {"response": result, "spoken": speak(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/listen")
async def listen_command(request: ListenRequest = None):
    """Listen for a voice command"""
    try:
        if request is None:
            request = ListenRequest()
            
        command = listen_for_command(timeout=request.timeout)
        
        if not command or "error" in command.lower() or "timeout" in command.lower():
            return {"success": False, "command": command}
        
        # Acknowledge with random phrase
        acknowledgement = choice(opening_text)
        speak(acknowledgement)
        
        result = process_command(command)
        return {
            "success": True,
            "command": command,
            "response": result,
            "spoken": speak(result)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/speak")
async def text_to_speech(request: SpeakRequest):
    """Convert text to speech"""
    try:
        spoken = speak(request.text)
        return {"success": True, "text": spoken}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/wikipedia")
async def wikipedia_search(request: WikipediaRequest):
    """Search for a topic on Wikipedia"""
    try:
        result = search_on_wikipedia(request.query)
        return {"success": True, "result": result, "spoken": speak(f"According to Wikipedia, {result}")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/youtube")
async def youtube_play(request: YoutubeRequest):
    """Play a video on YouTube"""
    try:
        result = play_on_youtube(request.query)
        return {"success": True, "result": result, "spoken": speak(f"Playing {request.query} on YouTube")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/google")
async def google_search(request: GoogleRequest):
    """Search on Google"""
    try:
        result = search_on_google(request.query)
        return {"success": True, "result": result, "spoken": speak(f"Searching for {request.query} on Google")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/weather")
async def weather_report(request: WeatherRequest):
    """Get weather report for a city"""
    try:
        weather, temperature, feels_like = get_weather_report(request.city)
        response = f"The current temperature in {request.city} is {temperature}, but it feels like {feels_like}. The weather is {weather}."
        return {"success": True, "weather": weather, "temperature": temperature, "feels_like": feels_like, "spoken": speak(response)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/email")
async def send_email_endpoint(request: EmailRequest):
    """Send an email"""
    try:
        success = send_email(request.receiver_address, request.subject, request.message)
        if success:
            response = "Email sent successfully"
        else:
            response = "Failed to send email"
        return {"success": success, "message": response, "spoken": speak(response)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/whatsapp")
async def send_whatsapp_endpoint(request: WhatsAppRequest):
    """Send a WhatsApp message"""
    try:
        success = send_whatsapp_message(request.number, request.message)
        if success:
            response = "WhatsApp message sent successfully"
        else:
            response = "Failed to send WhatsApp message"
        return {"success": success, "message": response, "spoken": speak(response)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 