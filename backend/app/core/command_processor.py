import re
from .utils import speak, get_time, get_date, get_weather
from ..functions.info_functions import (
    search_wikipedia, search_web, get_news,
    get_movie_info, ask_wolfram_alpha, get_joke
)
from ..functions.system_functions import (
    open_application, close_application, take_screenshot,
    get_system_info, open_website, create_reminder
)

class CommandProcessor:
    def __init__(self):
        self.commands = {
            # Time and date
            r'what (time|is the time)': lambda _: get_time(),
            r'what (date|is the date|day is it)': lambda _: get_date(),
            
            # Weather
            r'weather in (.+)': lambda match: get_weather(match.group(1).strip()),
            r'what\'s the weather in (.+)': lambda match: get_weather(match.group(1).strip()),
            r'how\'s the weather in (.+)': lambda match: get_weather(match.group(1).strip()),
            
            # Web search and information
            r'search for (.+) on wikipedia': lambda match: search_wikipedia(match.group(1)),
            r'wikipedia (.+)': lambda match: search_wikipedia(match.group(1)),
            r'search for (.+) on (web|google)': lambda match: search_web(match.group(0)),
            r'search (web|google) for (.+)': lambda match: search_web(match.group(0)),
            
            # News
            r'(get|tell me|what\'s the) (news|headlines)': lambda _: get_news(),
            
            # Movie info
            r'(tell me about|information about) the movie (.+)': lambda match: get_movie_info(match.group(2)),
            r'movie info(?:rmation)? (?:on|about) (.+)': lambda match: get_movie_info(match.group(1)),
            
            # Jokes
            r'tell (me )?(a )?joke': lambda _: get_joke(),
            r'make me laugh': lambda _: get_joke(),
            r'(say|tell) something funny': lambda _: get_joke(),

            # System apps
            r'open (.+)': lambda match: self._handle_open_command(match.group(1)),
            r'close (.+)': lambda match: close_application(match.group(1)),
            r'take (a )?screenshot': lambda _: take_screenshot(),
            r'(system|computer) information': lambda _: get_system_info(),
            r'what are my (system|computer) specs': lambda _: get_system_info(),
            
            # Reminders
            r'remind me to (.+)(?: at (.+))?': lambda match: create_reminder(
                match.group(1), match.group(2) if len(match.groups()) > 1 else None
            ),
            r'set a reminder for (.+)(?: at (.+))?': lambda match: create_reminder(
                match.group(1), match.group(2) if len(match.groups()) > 1 else None
            ),
            
            # General knowledge (Wolfram Alpha)
            r'(who|what|when|where|why|how) (.+)': lambda match: ask_wolfram_alpha(match.group(0)),
            r'calculate (.+)': lambda match: ask_wolfram_alpha(match.group(1)),
            r'compute (.+)': lambda match: ask_wolfram_alpha(match.group(1)),
        }
        
        # Add greeting patterns
        self.greeting_patterns = [
            r'hello', r'hi', r'hey', r'greetings', r'howdy'
        ]
        
        # Add exit patterns
        self.exit_patterns = [
            r'exit', r'quit', r'bye', r'goodbye', r'stop', r'end', r'terminate'
        ]
        
    def _handle_open_command(self, target):
        """
        Handle the 'open' command, differentiating between apps and websites
        """
        target = target.lower().strip()
        
        # Common website domains to check
        website_endings = ['.com', '.org', '.net', '.edu', '.gov', '.io']
        
        if any(ending in target for ending in website_endings) or 'website' in target or 'site' in target:
            # Extract website URL
            url = target.replace('website', '').replace('site', '').strip()
            return open_website(url)
        else:
            # Assume it's an application
            return open_application(target)
    
    def process_command(self, query):
        """
        Process a command and execute the appropriate function
        """
        if not query or query.isspace():
            return "I didn't receive a command."
        
        # Convert to lowercase for matching
        query = query.lower().strip()
        
        # Check for greetings
        for pattern in self.greeting_patterns:
            if re.match(pattern, query):
                return "Hello! How can I help you today?"
        
        # Check for exit commands
        for pattern in self.exit_patterns:
            if re.match(pattern, query):
                return "Goodbye! Have a nice day!"
        
        # Process other commands
        for pattern, handler in self.commands.items():
            match = re.search(pattern, query)
            if match:
                result = handler(match)
                return result
        
        # If no pattern matches, try Wolfram Alpha as a fallback
        try:
            return ask_wolfram_alpha(query)
        except:
            return f"I'm not sure how to help with '{query}'. Can you please try again?" 