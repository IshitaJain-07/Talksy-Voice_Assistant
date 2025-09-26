import os
import requests
import wikipedia
import pywhatkit as kit
import json
import wolframalpha
import pyjokes
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
WOLFRAM_ID = os.getenv("WOLFRAM_ALPHA_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

def search_wikipedia(query):
    """
    Search for a topic on Wikipedia and return a summary
    """
    try:
        query = query.replace("search for", "").replace("on wikipedia", "").strip()
        results = wikipedia.summary(query, sentences=3)
        return results
    except Exception as e:
        return f"An error occurred while searching Wikipedia: {str(e)}"

def search_web(query):
    """
    Perform a web search using PyWhatKit
    """
    try:
        search_term = query.replace("search for", "").replace("on web", "").replace("on google", "").strip()
        kit.search(search_term)
        return f"I've searched for '{search_term}' on Google."
    except Exception as e:
        return f"An error occurred while searching the web: {str(e)}"

def get_news():
    """
    Get the latest news headlines
    """
    api_key = NEWS_API_KEY
    if not api_key:
        return "News API key is not configured."
    
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        response = requests.get(url)
        news = response.json()
        
        if response.status_code != 200:
            return f"Error fetching news: {news.get('message', 'Unknown error')}"
        
        articles = news.get("articles", [])
        
        if not articles:
            return "No news articles found."
        
        headlines = []
        for i, article in enumerate(articles[:5], 1):
            headlines.append(f"{i}. {article['title']}")
        
        return "Here are the top headlines:\n" + "\n".join(headlines)
    
    except Exception as e:
        return f"An error occurred while getting the news: {str(e)}"

def get_movie_info(movie_name):
    """
    Get information about a movie
    """
    api_key = TMDB_API_KEY
    if not api_key:
        return "TMDB API key is not configured."
    
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200:
            return f"Error fetching movie info: {data.get('status_message', 'Unknown error')}"
        
        results = data.get("results", [])
        
        if not results:
            return f"No information found for '{movie_name}'."
        
        movie = results[0]  # Get the first result (most relevant)
        title = movie.get("title", "Unknown")
        overview = movie.get("overview", "No overview available")
        rating = movie.get("vote_average", "Unknown")
        release_date = movie.get("release_date", "Unknown")
        
        return f"Title: {title}\nRelease Date: {release_date}\nRating: {rating}/10\nOverview: {overview}"
    
    except Exception as e:
        return f"An error occurred while getting movie information: {str(e)}"

def ask_wolfram_alpha(query):
    """
    Query Wolfram Alpha for computational knowledge
    """
    app_id = WOLFRAM_ID
    if not app_id:
        return "Wolfram Alpha API key is not configured."
    
    try:
        client = wolframalpha.Client(app_id)
        res = client.query(query)
        answer = next(res.results).text
        
        if not answer:
            return "I couldn't find an answer to that question."
        
        return answer
    
    except Exception as e:
        return f"I couldn't process that with Wolfram Alpha: {str(e)}"

def get_joke():
    """
    Get a random joke
    """
    try:
        joke = pyjokes.get_joke()
        return joke
    except Exception as e:
        return f"I couldn't tell a joke right now: {str(e)}" 