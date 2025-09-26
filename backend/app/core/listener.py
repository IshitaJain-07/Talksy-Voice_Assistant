import speech_recognition as sr
import random
from .utils import speak

class SpeechListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 1  # Seconds of silence before the phrase is considered complete
        self.recognizer.energy_threshold = 300  # Minimum audio energy to consider for recording
        self.error_responses = [
            "Sorry, I didn't catch that.",
            "I couldn't understand what you said.",
            "Could you please repeat that?",
            "I missed what you said, please try again.",
            "I didn't quite get that, can you repeat it?"
        ]

    def take_command(self):
        """
        Listen for commands from the user
        """
        query = ""
        
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("Processing...")
                
                query = self.recognizer.recognize_google(audio, language='en-US')
                query = query.lower()
                print(f"User said: {query}")
                
        except sr.WaitTimeoutError:
            return "Timeout occurred while waiting for speech"
        except sr.UnknownValueError:
            error_message = random.choice(self.error_responses)
            speak(error_message)
            return error_message
        except sr.RequestError as e:
            error_message = f"Could not request results; {e}"
            speak(error_message)
            return error_message
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            speak(error_message)
            return error_message
            
        return query 