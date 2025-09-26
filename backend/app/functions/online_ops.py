import requests
import wikipedia
import pywhatkit as kit
import pyjokes
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys - set directly with fallback to .env values
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "e1d9d42731ee482ead7ad162e265c9ca")
OPENWEATHER_APP_ID = os.getenv("OPENWEATHER_APP_ID", "b2dfbfbe3ac672e26e6ebd9896d88453")
EMAIL = os.getenv("EMAIL", "janvimahajan0807@gmail.com")
PASSWORD = os.getenv("PASSWORD", "Janvi@86410")

def find_my_ip():
    """Get the external IP address"""
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]

def get_latest_news():
    """Get the latest news headlines"""
    api_key = NEWS_API_KEY
    if not api_key:
        return ["News API key is not configured."]
    
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        response = requests.get(url)
        news = response.json()
        
        if response.status_code != 200:
            return [f"Error fetching news: {news.get('message', 'Unknown error')}"]
        
        articles = news.get("articles", [])
        
        if not articles:
            return ["No news articles found."]
        
        return [article['title'] for article in articles[:5]]
    
    except Exception as e:
        return [f"An error occurred while getting the news: {str(e)}"]

def get_random_advice():
    """Get random advice"""
    try:
        res = requests.get("https://api.adviceslip.com/advice").json()
        return res['slip']['advice']
    except Exception as e:
        return f"Could not get advice at the moment: {str(e)}"

def get_random_joke():
    """Get a random joke"""
    try:
        return pyjokes.get_joke()
    except Exception as e:
        return f"I couldn't tell a joke right now: {str(e)}"

def get_weather_report(city):
    """Get weather data for a city"""
    api_key = OPENWEATHER_APP_ID
    if not api_key:
        return "Weather API not configured", "N/A", "N/A"
    
    try:
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
        
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code != 200:
            return f"Error getting weather data", "N/A", "N/A"
        
        weather_desc = data["weather"][0]["description"]
        temperature = f"{data['main']['temp']}°C"
        feels_like = f"{data['main']['feels_like']}°C"
        
        return weather_desc, temperature, feels_like
    except Exception as e:
        return f"Error getting weather data: {str(e)}", "N/A", "N/A"

def play_on_youtube(video):
    """Play a video on YouTube"""
    try:
        kit.playonyt(video)
        return f"Playing {video} on YouTube"
    except Exception as e:
        return f"An error occurred while trying to play on YouTube: {str(e)}"

def search_on_google(query):
    """Search on Google"""
    try:
        kit.search(query)
        return f"Searching for {query} on Google"
    except Exception as e:
        return f"An error occurred while searching the web: {str(e)}"

def search_on_wikipedia(query):
    """Search for a topic on Wikipedia and return a summary"""
    try:
        results = wikipedia.summary(query, sentences=2)
        return results
    except Exception as e:
        return f"An error occurred while searching Wikipedia: {str(e)}"

def send_email(receiver_address, subject, message):
    """Send an email"""
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        sender_email = EMAIL
        password = PASSWORD
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_address
        msg['Subject'] = subject
        
        # Attach message body
        msg.attach(MIMEText(message, 'plain'))
        
        # Connect to Gmail server
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(sender_email, receiver_address, text)
            server.quit()
            return True
        except Exception as e:
            print(f"SMTP Error: {str(e)}")
            # Fall back to pywhatkit email if SMTP fails
            try:
                kit.send_mail(sender_email, password, subject, message, receiver_address)
                return True
            except:
                return False
    except Exception as e:
        print(f"Error in sending email: {str(e)}")
        return False

def send_whatsapp_message(number, message):
    """Send a WhatsApp message"""
    try:
        kit.sendwhatmsg_instantly(f"+{number}", message)
        return True
    except Exception as e:
        print(f"Error in sending whatsapp message: {str(e)}")
        return False 