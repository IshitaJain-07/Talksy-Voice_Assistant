# Talksy Backend

The backend for Talksy, a privacy-focused virtual assistant that works offline.

## Features

- Voice recognition and command processing
- Text-to-speech capabilities
- Multiple utility functions including:
  - Web searches
  - Weather information
  - System controls
  - Application management
  - And more!

## Setup

1. Install the required dependencies:
   ```
   pip install -r ../requirements.txt
   ```

2. Create a `.env` file in the backend directory with the following variables:
   ```
   USER=YourName
   BOTNAME=Talksy
   EMAIL=your_email@example.com
   PASSWORD=your_password
   NEWS_API_KEY=your_news_api_key
   OPENWEATHER_APP_ID=your_openweather_api_key
   TMDB_API_KEY=your_tmdb_api_key
   WOLFRAM_ALPHA_ID=your_wolfram_alpha_id
   ```

3. Run the application:
   ```
   python run.py
   ```

## API Endpoints

- `GET /` - Root endpoint with welcome message
- `GET /greet` - Get a greeting based on time of day
- `POST /process-text` - Process a text command
- `POST /listen` - Listen for a voice command
- `POST /speak` - Convert text to speech

## Architecture

- `app/core/` - Core functionality (speech processing, commands)
- `app/functions/` - Specific function implementations
- `app/routers/` - API route definitions
- `app/main.py` - FastAPI application setup 